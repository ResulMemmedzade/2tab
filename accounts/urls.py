from django.urls import path
from .views import *

urlpatterns = [
    path('', dashboard, name='dashboard'),

    path('menim-kitablarim/', my_books, name='my_books'),
    path('menim-kitablarim/kitab-elave-et/', book_create, name='book_create'),
    path('menim-kitablarim/<slug:slug>/edit/', book_update, name='book_update'),
    path('menim-kitablarim/<slug:slug>/sil/', book_delete, name='book_delete'),

    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
]