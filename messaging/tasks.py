# messaging/tasks.py
import json
import logging
from celery import shared_task
from pywebpush import webpush, WebPushException
from django.conf import settings
from .models import Conversation

logger = logging.getLogger(__name__)

@shared_task
def send_delayed_notification(conversation_id, receiver_id):
    try:
        conversation = Conversation.objects.get(id=conversation_id)
    except Conversation.DoesNotExist:
        return "Söhbət tapılmadı."

    # Oxunmamış mesajları yoxlayırıq
    unread_messages = conversation.messages.exclude(sender_id=receiver_id).filter(read_at__isnull=True)
    count = unread_messages.count()

    # Əgər adam artıq mesajları oxuyubsa, prosesi dayandırırıq
    if count == 0:
        return "Mesajlar artıq oxunub, bildiriş ləğv edildi."

    last_msg = unread_messages.last()
    receiver = conversation.participants.get(id=receiver_id)

    # Bildiriş ayarlarını yoxlayırıq
    if hasattr(receiver, 'notification_preference') and not receiver.notification_preference.is_enabled:
        return "İstifadəçi bildirişləri deaktiv edib."

    # Bildiriş mətni və qruplaşdırma
    sender_name = last_msg.sender.name
    title = sender_name if count == 1 else f"{sender_name} ({count} yeni mesaj)"
    body = last_msg.text if last_msg.text else "📷 Şəkil göndərdi"

    # Frontend-dəki Service Worker-in alacağı Payload (JSON)
    payload_data = {
        "title": title,
        "body": body,
        "icon": "/static/images/logo.png", # Öz loqonun yolu
        "url": f"/panel/mesajlar/{conversation_id}/"
    }

    # İstifadəçinin bütün aktiv browser abonəliklərini (cihazlarını) tapırıq
    subscriptions = receiver.push_subscriptions.all()
    if not subscriptions.exists():
        return "İstifadəçinin aktiv bildiriş abonəliyi (cihazı) yoxdur."

    success_count = 0
    for sub in subscriptions:
        try:
            webpush(
                subscription_info={
                    "endpoint": sub.endpoint,
                    "keys": {
                        "p256dh": sub.p256dh,
                        "auth": sub.auth
                    }
                },
                data=json.dumps(payload_data),
                vapid_private_key=settings.WEBPUSH_SETTINGS["VAPID_PRIVATE_KEY"],
                vapid_claims={"sub": settings.WEBPUSH_SETTINGS["VAPID_ADMIN_EMAIL"]}
            )
            success_count += 1
            
        except WebPushException as ex:
            # Əgər xəta kodu 404 (Tapılmadı) və ya 410 (Gone - vaxtı bitib/ləğv edilib) olarsa,
            # bu o deməkdir ki, istifadəçi browserdən icazəni silib. Biz də bazadan silirik.
            if ex.response is not None and ex.response.status_code in [404, 410]:
                logger.info(f"Yarasız abonəlik silindi: {sub.endpoint}")
                sub.delete()
            else:
                logger.error(f"Web Push Xətası: {repr(ex)}")
        except Exception as e:
            logger.error(f"Bilinməyən Web Push Xətası: {str(e)}")

    return f"Bildirişlər {success_count} cihaza göndərildi."