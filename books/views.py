from django.shortcuts import get_object_or_404, redirect, render
from .models import Book
# Create your views here.

def index(request):
    books = Book.objects.prefetch_related('images')[:10]
    return render(request, 'index.html', {'books': books,})


def book_detail(request, slug):
    book = get_object_or_404(Book.objects.select_related('owner').prefetch_related('images'),slug=slug)

    is_favorite = (request.user.is_authenticated and book.favorite_users.filter(pk=request.user.pk).exists())

    context={
        'book': book,
        'is_favorite': is_favorite,
    }

    return render(request,'books/book_detail.html',context)

def book_list(request):
    books = Book.objects.prefetch_related('images')
    return render(request, 'index.html', {'books': books,})

def contact_us(request):
    return render(request, "books/contact_us.html")