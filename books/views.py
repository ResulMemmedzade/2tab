from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from django.http import JsonResponse
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


    search = request.GET.get('search', '').strip()
    genre = request.GET.get('genre', '').strip()
    condition = request.GET.get('condition', '').strip()
    language = request.GET.get('language', '').strip()
    sort = request.GET.get('sort', 'newest').strip()


    if search:
        books = books.filter(
            Q(title__icontains=search) |
            Q(author_name__icontains=search) |
            Q(description__icontains=search)
        )


    if genre:
        books = books.filter(genre=genre)


    if condition:
        books = books.filter(condition=condition)


    if language:
        books = books.filter(language=language)


    sort_options = {
        'newest': '-created_at',
        'oldest': 'created_at',
        'price_asc': 'price',
        'price_desc': '-price',
        'title_asc': 'title',
        'title_desc': '-title',
    }

    books = books.order_by(
        sort_options.get(sort, '-created_at')
    )

    context={
                'books': books,
                'search': search,
                'genre': genre,
                'condition': condition,
                'language': language,
                'sort': sort,
            }

    return render(request,'books/book_list.html',context)

def contact_us(request):
    return render(request, "books/contact_us.html")



@login_required
def toggle_favorite(request, slug):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=405)

    book = get_object_or_404(Book, slug=slug)
    user = request.user

    if book.favorite_users.filter(id=user.id).exists():
        book.favorite_users.remove(user)
        is_favorite = False
    else:
        book.favorite_users.add(user)
        is_favorite = True

    return JsonResponse({
        "success": True,
        "is_favorite": is_favorite,
    })


@login_required
def favorite_books(request):
    books = request.user.favorite_books.select_related("owner").prefetch_related("images").all()

    return render(request, "books/favourites.html", {
        "books": books,
    })