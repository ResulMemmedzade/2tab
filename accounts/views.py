from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login, authenticate, logout
from django.core.cache import cache
from books.models import *
from .forms import *


@login_required
def dashboard(request):
    return render(request, 'accounts'
    '/dashboard.html')

@login_required
def my_books(request):
    books = request.user.books.select_related("owner").prefetch_related("images").all()

    return render(request, "accounts/my_books.html", {"books": books,})

@login_required
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        formset = BookImageFormSet(request.POST, request.FILES)

        if form.is_valid() and formset.is_valid():
            book = form.save(commit=False)
            book.owner = request.user
            book.save()

            formset.instance = book
            formset.save()

            return redirect('book_detail', slug=book.slug)

    else:
        form = BookForm()
        formset = BookImageFormSet()

    return render(request, 'accounts/book_create.html', {
        'form': form,
        'formset': formset,
    })

@login_required
def book_update(request, slug):
    book = get_object_or_404(
        Book,
        slug=slug,
        owner=request.user
    )

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        formset = BookImageFormSet(
            request.POST,
            request.FILES,
            instance=book
        )

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()

            return redirect('book_detail', slug=book.slug)

    else:
        form = BookForm(instance=book)
        formset = BookImageFormSet(instance=book)

    return render(request, 'accounts/book_update.html', {
        'form': form,
        'formset': formset,
        'book': book,
        'title': 'Kitabı redaktə et',
    })


@login_required
def book_delete(request, slug):
    book = get_object_or_404(Book,slug=slug,owner=request.user)

    if request.method == 'POST':
        book.delete()
        return redirect('my_books')

    return render(request, 'accounts/book_update.html', {'book': book})



def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# accounts/views.py

def register_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            
            user.backend = 'accounts.backends.EmailModelBackend'
            
            login(request, user)
            return redirect('index')

    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})
def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    ip = get_client_ip(request)
    cache_key = f"login_attempts_{ip}"
    
    attempts = cache.get(cache_key, 0)
    
    if attempts >= 5:
        error_message = "Çox sayda uğursuz cəhd etdiniz. Zəhmət olmasa 1 saat sonra yenidən yoxlayın."
        return render(request, 'accounts/login.html', {'form': LoginForm(), 'error_message': error_message})

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                cache.delete(cache_key)
                login(request, user)
                return redirect('dashboard')
            else:
                attempts += 1
                if attempts >= 5:
                    cache.set(cache_key, attempts, timeout=3600)
                    error_message = "Çox sayda uğursuz cəhd etdiniz. Zəhmət olmasa 1 saat sonra yenidən yoxlayın."
                else:
                    cache.set(cache_key, attempts, timeout=300)
                    error_message = f"Məlumatlar yanlışdır. Qalan cəhd sayınız: {5 - attempts}"
                
                return render(request, 'accounts/login.html', {'form': form, 'error_message': error_message})
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')