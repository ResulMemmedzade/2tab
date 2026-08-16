# messaging/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('start/<int:user_id>/', views.start_chat, name='start_chat'),
    path('<int:conversation_id>/', views.chat_room, name='chat_room'),
    

    path('<int:conversation_id>/upload-image/', views.upload_image, name='upload_image'),
    path('message/<int:message_id>/edit/', views.edit_message, name='edit_message'),
    path('message/<int:message_id>/delete/', views.delete_message, name='delete_message'),
    path('<int:conversation_id>/load-more/', views.load_more_messages, name='load_more_messages'),
    path('push/save-subscription/', views.save_push_subscription, name='save_push_subscription'),
    path('push/toggle/', views.toggle_notifications, name='toggle_notifications'),
    path('push/vapid-public-key/', views.get_vapid_public_key, name='vapid_public_key'),
    path('start-admin-chat/', views.start_chat_with_admin, name='start_chat_with_admin'),
    path('start-user-chat/<int:user_id>/', views.start_chat_with_user, name='start_chat_with_user'),
]