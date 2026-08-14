from django.db import models
from django.utils.text import slugify
from accounts.models import CustomUser


class Book(models.Model):

    class Language(models.TextChoices):
        AZERBAIJANI = "az", "Azərbaycan"
        ENGLISH = "en", "İngilis"
        RUSSIAN = "ru", "Rus"
        TURKISH = "tr", "Türk"
    class Condition(models.TextChoices):
        NEW = 'new', 'Yeni'
        LIKE_NEW = 'like_new', 'Yeni kimi'
        MEDIUM = 'medium', 'Orta'
        LIKE_OLD = 'like_old', 'Köhnə kimi'
        OLD = 'old', 'Köhnə'

    class Genre(models.TextChoices):
        FICTION = "fiction", "Bədii"
        FANTASY = "fantasy", "Fantastika"
        SCIENCE_FICTION = "science_fiction", "Elmi fantastika"
        MYSTERY = "mystery", "Detektiv"
        THRILLER = "thriller", "Triller"
        ROMANCE = "romance", "Romantik"
        HORROR = "horror", "Qorxu"
        HISTORY = "history", "Tarix"
        BIOGRAPHY = "biography", "Bioqrafiya"
        SELF_HELP = "self_help", "Şəxsi inkişaf"
        PHILOSOPHY = "philosophy", "Fəlsəfə"
        PSYCHOLOGY = "psychology", "Psixologiya"
        SCIENCE = "science", "Elmi"
        BUSINESS = "business", "Biznes"
        CHILDREN = "children", "Uşaq ədəbiyyatı"

    slug = models.SlugField(unique=True, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    author_name = models.CharField(max_length=100)

    price = models.DecimalField(max_digits=6, decimal_places=2)
    condition = models.CharField(max_length=20, choices=Condition.choices, default=Condition.MEDIUM)
    genre = models.CharField(max_length=20, choices=Genre.choices)
    language = models.CharField(max_length=5,choices=Language.choices,default=Language.AZERBAIJANI)

    owner = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='books')
    created_at = models.DateTimeField(auto_now_add=True)
    favorite_users = models.ManyToManyField(CustomUser, related_name='favorite_books', blank=True)

    @property
    def cover_image(self):
        return self.images.first()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title) or "book"
        super().save(*args, **kwargs)


    class Meta:
        verbose_name_plural = 'Books'
        ordering = ['-created_at']

class BookImage(models.Model):
    book = models.ForeignKey(Book,on_delete=models.CASCADE,related_name='images')
    image = models.ImageField(upload_to='books/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.book.title} - Image"