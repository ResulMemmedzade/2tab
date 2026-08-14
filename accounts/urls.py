from django.urls import path
from .views import *
urlpatterns = [
    path('',dashboard,name='dashboard'),
    # path('menim-kitablarim',my_books,name='my_books'),
    # path('favorilerim',favourites,name='favourites'),
    # path('cixis',log_out,name='log_out'),
    # path('mesajlarim',chats,name='chats'),
    # path('kitab-elave-et',add_new_book,name='add_new_book')
]