from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.core.cache import cache
from django.conf import settings
from django.db.models import Count, Q
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from PIL import Image, ImageOps
from io import BytesIO
import json

from .models import Conversation, Message
from .tasks import send_delayed_notification
from .models import PushSubscription, NotificationPreference

@login_required
def inbox(request):
    conversations = request.user.conversations.annotate(
        unread_count=Count(
            'messages',
            filter=Q(messages__read_at__isnull=True) & ~Q(messages__sender=request.user)
        )
    ).order_by('-updated_at')
    
    return render(request, 'messaging/inbox.html', {'conversations': conversations})

@login_required
def start_chat(request, user_id):
    User = get_user_model() # bura əlavə edildi
    other_user = get_object_or_404(User, id=user_id)

    conversation = (Conversation.objects.filter(participants=request.user).filter(participants=other_user).first())

    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, other_user)

    return redirect("chat_room", conversation_id=conversation.id)

@login_required
def chat_room(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
    messages = conversation.messages.all()

    unread_messages = messages.exclude(sender=request.user).filter(read_at__isnull=True)
    unread_messages.update(read_at=timezone.now())

    other_user = conversation.participants.exclude(id=request.user.id).first()

    return render(request, "messaging/chat.html", {"conversation": conversation, "messages": messages, "other_user": other_user})

@login_required
def upload_image(request, conversation_id):
    if request.method == "POST" and request.FILES.get("image"):
        conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
        image = request.FILES["image"]
        img = Image.open(image)
        img = ImageOps.exif_transpose(img)

        if img.mode != "RGB":
            img = img.convert("RGB")

        img.thumbnail((1200, 1200), Image.Resampling.LANCZOS)
        output = BytesIO()
        img.save(output, format="JPEG", quality=85, optimize=True)
        output.seek(0)

        optimized_image = InMemoryUploadedFile(
            output, "ImageField", f"{image.name.rsplit('.', 1)[0]}.jpg", "image/jpeg", output.getbuffer().nbytes, None
        )

        message = Message.objects.create(conversation=conversation, sender=request.user, image=optimized_image)
        receiver = conversation.participants.exclude(id=request.user.id).first()

        if receiver:
            lock_key = f"notify_lock_{conversation.id}_{receiver.id}"
            if cache.add(lock_key, "locked", timeout=3):
                send_delayed_notification.apply_async((conversation.id, receiver.id), countdown=3)

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"chat_{conversation.id}",
            {
                "type": "chat_message",
                "message": "",
                "image_url": message.image.url,
                "sender_name": request.user.name,
                "sender_id": request.user.id,
                "message_id": message.id,
                "created_at": message.created_at.strftime("%H:%M")
            }
        )
        return JsonResponse({"success": True, "message_id": message.id, "image_url": message.image.url})

    return JsonResponse({"error": "Yanlış sorğu"}, status=400)

@login_required
def edit_message(request, message_id):
    if request.method == "POST":
        message = get_object_or_404(Message, id=message_id, sender=request.user)
        data = json.loads(request.body)
        new_text = data.get("text")

        if new_text and not message.is_deleted:
            message.text = new_text
            message.is_edited = True
            message.save()

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"chat_{message.conversation.id}",
                {"type": "message_edited", "message_id": message.id, "new_text": new_text}
            )
            return JsonResponse({"success": True})
    return JsonResponse({"error": "Yanlış sorğu"}, status=400)

@login_required
def delete_message(request, message_id):
    if request.method == "POST":
        message = get_object_or_404(Message, id=message_id, sender=request.user)
        message.is_deleted = True
        message.text = "Bu mesaj silinib"

        if message.image:
            message.image.delete()

        message.save()

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"chat_{message.conversation.id}",
            {"type": "message_deleted", "message_id": message.id}
        )
        return JsonResponse({"success": True})
    return JsonResponse({"error": "Yanlış sorğu"}, status=400)

@login_required
def load_more_messages(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
    before_id = request.GET.get("before_id")
    messages = conversation.messages.all().order_by("-created_at")

    if before_id:
        messages = messages.filter(id__lt=before_id)

    messages = messages[:30]
    messages_data = []

    for msg in messages:
        messages_data.append({
            "id": msg.id,
            "sender_id": msg.sender.id,
            "sender_name": msg.sender.name,
            "text": msg.text,
            "image_url": msg.image.url if msg.image else None,
            "is_edited": msg.is_edited,
            "is_deleted": msg.is_deleted,
            "created_at": msg.created_at.strftime("%H:%M"),
            "read_at": msg.read_at.strftime("%H:%M") if msg.read_at else None,
        })

    messages_data.reverse()
    return JsonResponse({"messages": messages_data})

@login_required
def save_push_subscription(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        endpoint = data.get('endpoint')
        keys = data.get('keys', {})
        p256dh = keys.get('p256dh')
        auth = keys.get('auth')

        if endpoint and p256dh and auth:
            PushSubscription.objects.get_or_create(
                user=request.user, endpoint=endpoint, defaults={'p256dh': p256dh, 'auth': auth}
            )
            return JsonResponse({'success': True})
    return JsonResponse({'error': 'Yanlış sorğu'}, status=400)

@login_required
def toggle_notifications(request):
    if request.method == 'POST':
        pref, created = NotificationPreference.objects.get_or_create(user=request.user)
        pref.is_enabled = not pref.is_enabled
        pref.save()
        return JsonResponse({'success': True, 'is_enabled': pref.is_enabled})
    return JsonResponse({'error': 'Yanlış sorğu'}, status=400)

@login_required
def get_vapid_public_key(request):
    return JsonResponse({'public_key': settings.WEBPUSH_SETTINGS['VAPID_PUBLIC_KEY']})

@login_required
def start_chat_with_admin(request):
    User = get_user_model() # bura əlavə edildi
    admin_user = User.objects.filter(is_superuser=True).first()
    
    if not admin_user:
        admin_user = User.objects.filter(is_staff=True).first()
        
    if not admin_user or admin_user == request.user:
        return redirect('inbox')
        
    conversation = Conversation.objects.filter(participants=request.user).filter(participants=admin_user).first()
    
    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, admin_user)
        
    return redirect('chat_room', conversation_id=conversation.id)

@login_required
def start_chat_with_user(request, user_id):
    User = get_user_model() # bura əlavə edildi
    other_user = get_object_or_404(User, id=user_id)
    
    if other_user == request.user:
        return redirect('inbox')
        
    conversation = Conversation.objects.filter(participants=request.user).filter(participants=other_user).first()
    
    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, other_user)
        
    return redirect('chat_room', conversation_id=conversation.id)