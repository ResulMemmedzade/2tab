from messaging.models import Message

def unread_message_count(request):
    if not request.user.is_authenticated:
        return {'unread_message_count': 0}

    # İstifadəçiyə gələn və hələ oxunmamış bütün mesajların sayı
    count = Message.objects.filter(
        conversation__participants=request.user,
        read_at__isnull=True
    ).exclude(sender=request.user).count()

    return {'unread_message_count': count}