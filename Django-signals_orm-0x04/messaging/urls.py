from django.urls import path
from . import views

urlpatterns = [
    path('conversation/<uuid:user_id>/', views.conversation_messages, name='conversation_messages'),
    path('delete-user/', views.delete_user, name='delete_user'),
    path('unread-messages/', views.unread_messages, name='unread_messages'),
    path('message-history/<uuid:message_id>/', views.message_history, name='message_history'),
]
