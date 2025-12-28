"""
Admin Panel app URL configuration.
"""

from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    # Dashboard
    path('', views.DashboardView.as_view(), name='dashboard'),
    
    # User Management
    path('users/', views.UserListView.as_view(), name='users'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
    path('users/<int:pk>/toggle-status/', views.ToggleUserStatusView.as_view(), name='toggle_user_status'),
    path('users/<int:pk>/ban/', views.BanUserView.as_view(), name='ban_user'),
    
    # Property Management
    path('properties/', views.PropertyListView.as_view(), name='properties'),
    path('properties/pending/', views.PendingPropertiesView.as_view(), name='pending_properties'),
    path('properties/<int:pk>/', views.PropertyDetailView.as_view(), name='property_detail'),
    path('properties/<int:pk>/approve/', views.ApprovePropertyView.as_view(), name='approve_property'),
    path('properties/<int:pk>/reject/', views.RejectPropertyView.as_view(), name='reject_property'),
    path('properties/<int:pk>/delete/', views.DeletePropertyView.as_view(), name='delete_property'),
    path('properties/bulk-action/', views.BulkPropertyActionView.as_view(), name='bulk_property_action'),
    
    # Inquiry Management
    path('inquiries/', views.InquiryListView.as_view(), name='inquiries'),
    path('inquiries/<int:pk>/', views.InquiryDetailView.as_view(), name='inquiry_detail'),
    
    # Service Requests
    path('services/find-room/', views.FindRoomRequestListView.as_view(), name='find_room_requests'),
    path('services/find-room/<int:pk>/', views.FindRoomRequestDetailView.as_view(), name='find_room_detail'),
    path('services/shift-home/', views.ShiftHomeRequestListView.as_view(), name='shift_home_requests'),
    path('services/shift-home/<int:pk>/', views.ShiftHomeRequestDetailView.as_view(), name='shift_home_detail'),
    
    # Reports
    path('reports/', views.ReportListView.as_view(), name='reports'),
    path('reports/<int:pk>/', views.ReportDetailView.as_view(), name='report_detail'),
    path('reports/<int:pk>/resolve/', views.ResolveReportView.as_view(), name='resolve_report'),
    
    # Analytics
    path('analytics/', views.AnalyticsView.as_view(), name='analytics'),
    
    # Activity Log
    path('activity-log/', views.ActivityLogView.as_view(), name='activity_log'),
]
