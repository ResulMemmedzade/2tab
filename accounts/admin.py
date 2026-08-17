from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'phone_number', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'name', 'phone_number')
    ordering = ('email',)
    list_editable = ('is_active', 'is_staff') # Paneldən çıxmadan bir kliklə aktiv/deaktiv etmək üçün
    
    # Detallı baxış səhifəsindəki düzülüş
    fieldsets = (
        ('Şəxsi Məlumatlar', {'fields': ('email', 'name', 'phone_number', 'profile_picture')}),
        ('İcazələr və Status', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Təhlükəsizlik', {'fields': ('password_change_count', 'password_change_period_start', 'password')}),
        ('Tarixlər', {'fields': ('last_login', 'date_joined')}),
    )
    readonly_fields = ('last_login', 'date_joined')