from django.db.models import Count, Q


def unread_message_count(request):
    if not request.user.is_authenticated:
        return {'unread_message_count': 0}

    count = request.user.conversations.filter(
        messages__read_at__isnull=True
    ).exclude(
        messages__sender=request.user
    ).distinct().count()

    return {'unread_message_count': count}