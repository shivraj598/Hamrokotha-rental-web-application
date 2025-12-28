"""
Services app URL configuration.
"""

from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    # Find Room Service
    path('find-room/', views.FindRoomRequestView.as_view(), name='find_room'),
    path('find-room/success/', views.FindRoomSuccessView.as_view(), name='find_room_success'),
    
    # Shift Home Service
    path('shift-home/', views.ShiftHomeRequestView.as_view(), name='shift_home'),
    path('shift-home/success/', views.ShiftHomeSuccessView.as_view(), name='shift_home_success'),
    
    # My Requests
    path('my-requests/', views.MyRequestsView.as_view(), name='my_requests'),
]
