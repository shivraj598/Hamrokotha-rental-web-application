from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    # Services Home
    path('', views.ServicesHomeView.as_view(), name='home'),
    
    # Find Room Service
    path('find-room/', views.FindRoomCreateView.as_view(), name='find_room'),
    path('find-room/success/<uuid:pk>/', views.FindRoomSuccessView.as_view(), name='find_room_success'),
    path('find-room/my-requests/', views.FindRoomListView.as_view(), name='find_room_list'),
    path('find-room/<uuid:pk>/', views.FindRoomDetailView.as_view(), name='find_room_detail'),
    
    # Shift Home Service
    path('shift-home/', views.ShiftHomeCreateView.as_view(), name='shift_home'),
    path('shift-home/success/<uuid:pk>/', views.ShiftHomeSuccessView.as_view(), name='shift_home_success'),
    path('shift-home/my-requests/', views.ShiftHomeListView.as_view(), name='shift_home_list'),
    path('shift-home/<uuid:pk>/', views.ShiftHomeDetailView.as_view(), name='shift_home_detail'),
]
