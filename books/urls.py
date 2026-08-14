from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('',index,name='index'),
    path('kitablar',book_list,name='book_list'),
    path("kitablar/<slug:slug>/", book_detail, name="book_detail"),
    path("kitablar/<slug:slug>/sevimliler/",toggle_favorite,name="toggle_favorite"),
    path('bizimle-elaqe',contact_us,name='contact_us'),
    path('favoriler',favorite_books,name='favourite_books'),
    
]

