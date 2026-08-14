from django.contrib import admin
from .models import Book, BookImage


class BookImageInline(admin.TabularInline):
    model = BookImage
    extra = 1  # Standart olaraq 1 boş şəkil sahəsi göstərir
    readonly_fields = ('created_at',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author_name', 'price', 'genre', 'condition', 'owner', 'created_at')
    search_fields = ('title', 'author_name', 'description')
    list_filter = ('genre', 'condition', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('favorite_users',)
    list_per_page = 20

    # Şəkil yükləmə blokunu kitab səhifəsinə daxil edirik
    inlines = [BookImageInline]