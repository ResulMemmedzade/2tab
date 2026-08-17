# DOĞRUDUR
from django.db import models
from django.conf import settings  # Bunu import edin

class Conversation(models.Model):
    # User əvəzinə settings.AUTH_USER_MODEL yazın
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"Söhbət: {self.id}"

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    # User əvəzinə settings.AUTH_USER_MODEL yazın
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='chat_images/', blank=True, null=True)
    read_at = models.DateTimeField(null=True, blank=True)
    is_edited = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        text = self.text or "[Şəkil]"
        # settings.AUTH_USER_MODEL string olduğu üçün self.sender.name olduğu kimi qalır, o model instansiyasıdır
        return f"{self.sender.name}: {text[:20]}"

class PushSubscription(models.Model):
    # User əvəzinə settings.AUTH_USER_MODEL
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='push_subscriptions')
    endpoint = models.URLField(max_length=500)
    p256dh = models.CharField(max_length=100)
    auth = models.CharField(max_length=100)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} - cihazı"

class NotificationPreference(models.Model):
    # User əvəzinə settings.AUTH_USER_MODEL
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notification_preference')
    is_enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.name} - Bildirişlər: {'Açıq' if self.is_enabled else 'Bağlı'}"