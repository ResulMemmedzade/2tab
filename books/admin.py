from django.contrib import admin
from .models import Book, BookImage

class BookImageInline(admin.TabularInline):
    model = BookImage
    extra = 1 # Avtomatik olaraq 1 ədəd boş şəkil yükləmə qutusu göstərir

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author_name', 'owner', 'price', 'condition', 'genre', 'language', 'created_at')
    list_filter = ('condition', 'genre', 'language', 'created_at')
    search_fields = ('title', 'author_name', 'owner__email', 'owner__name')
    ordering = ('-created_at',)
    
    # Kitabın detallarına girəndə şəkilləri də orada göstərsin
    inlines = [BookImageInline]
    
    # Slug avtomatik yaranır deyə onu dəyişilməz (readonly) edirik ki, xəta çıxmasın
    readonly_fields = ('slug', 'created_at')