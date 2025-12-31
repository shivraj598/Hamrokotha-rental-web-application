from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    # Services Home
    path('', views.ServicesHomeView.as_view(), name='home'),
    
    # Find Room Service - Tenant posts room requests
    path('find-room/', views.FindRoomCreateView.as_view(), name='find_room'),
    path('find-room/my-requests/', views.MyRoomRequestsView.as_view(), name='my_room_requests'),
    path('find-room/<uuid:pk>/close/', views.CloseRoomRequestView.as_view(), name='close_room_request'),
    path('find-room/<uuid:pk>/delete/', views.DeleteRoomRequestView.as_view(), name='delete_room_request'),
    
    # Room Requests - Landlords view tenant requests
    path('room-requests/', views.RoomRequestListView.as_view(), name='room_requests'),
    path('room-requests/<uuid:pk>/', views.RoomRequestDetailView.as_view(), name='room_request_detail'),
    path('room-requests/<uuid:pk>/reply/', views.RoomRequestReplyView.as_view(), name='room_request_reply'),
    
    # Shift Home Service
    path('shift-home/', views.ShiftHomeCreateView.as_view(), name='shift_home'),
    path('shift-home/success/<uuid:pk>/', views.ShiftHomeSuccessView.as_view(), name='shift_home_success'),
    path('shift-home/my-requests/', views.ShiftHomeListView.as_view(), name='shift_home_list'),
    path('shift-home/<uuid:pk>/', views.ShiftHomeDetailView.as_view(), name='shift_home_detail'),
    path('shift-home/<uuid:pk>/delete/', views.DeleteShiftHomeRequestView.as_view(), name='delete_shift_home_request'),
    
    # Legacy URLs for compatibility
    path('find-room/success/<uuid:pk>/', views.RoomRequestDetailView.as_view(), name='find_room_success'),
    path('find-room/my-requests-legacy/', views.MyRoomRequestsView.as_view(), name='find_room_list'),
    path('find-room/<uuid:pk>/', views.RoomRequestDetailView.as_view(), name='find_room_detail'),
]
