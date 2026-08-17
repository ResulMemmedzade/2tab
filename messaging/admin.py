from django.contrib import admin
from .models import Conversation, Message, PushSubscription, NotificationPreference

class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    # Mesajları admin paneldən səhvən dəyişməmək üçün yalnız oxunur edirik
    readonly_fields = ('sender', 'text', 'image', 'created_at', 'read_at', 'is_edited', 'is_deleted')
    can_delete = False
    classes = ('collapse',) # Çox mesaj olanda səhifəni dondurmasın deyə qatlanan (collapse) formada edirik

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_participants', 'created_at', 'updated_at')
    inlines = [MessageInline]
    ordering = ('-updated_at',)

    # ManyToMany (Çoxlu) əlaqəni ekranda göstərmək üçün xüsusi funksiya
    def get_participants(self, obj):
        return ", ".join([p.name for p in obj.participants.all()])
    get_participants.short_description = 'İştirakçılar'

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'conversation', 'sender', 'short_text', 'is_read', 'is_deleted', 'created_at')
    list_filter = ('is_deleted', 'is_edited', 'created_at')
    search_fields = ('text', 'sender__name', 'sender__email')
    ordering = ('-created_at',)

    def short_text(self, obj):
        return obj.text[:50] + '...' if obj.text else '(Şəkil Göndərilib)'
    short_text.short_description = 'Mesaj'

    def is_read(self, obj):
        return bool(obj.read_at)
    is_read.boolean = True # Ekranda Yes/No ikonu kimi (Yaşıl quş/Qırmızı çarpaz) görünməsi üçün
    is_read.short_description = 'Oxunub'

@admin.register(PushSubscription)
class PushSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user__name', 'user__email')

@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_enabled')
    list_editable = ('is_enabled',)
    search_fields = ('user__name', 'user__email')