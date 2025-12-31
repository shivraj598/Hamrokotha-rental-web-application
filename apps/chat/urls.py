"""
Chat app URL configuration.
"""

from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    # Chat list
    path('', views.ChatListView.as_view(), name='list'),
    
    # Chat room
    path('<uuid:pk>/', views.ChatRoomView.as_view(), name='room'),
    
    # Start chat with a user
    path('start/<int:user_id>/', views.StartChatView.as_view(), name='start'),
    path('start/<int:user_id>/property/<uuid:property_id>/', views.StartChatView.as_view(), name='start_with_property'),
    
    # AJAX endpoints
    path('<uuid:pk>/send/', views.SendMessageView.as_view(), name='send_message'),
    path('<uuid:pk>/messages/', views.GetMessagesView.as_view(), name='get_messages'),
    path('unread-count/', views.GetUnreadCountView.as_view(), name='unread_count'),
]
