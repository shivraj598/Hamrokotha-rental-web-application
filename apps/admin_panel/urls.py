from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    # Dashboard
    path('', views.DashboardView.as_view(), name='dashboard'),
    
    # Property Management
    path('properties/', views.PropertyManagementView.as_view(), name='properties'),
    path('properties/<uuid:pk>/approve/', views.PropertyApproveView.as_view(), name='approve_property'),
    path('properties/<uuid:pk>/reject/', views.PropertyRejectView.as_view(), name='reject_property'),
    path('properties/<uuid:pk>/toggle-featured/', views.PropertyToggleFeaturedView.as_view(), name='toggle_featured'),
    
    # User Management
    path('users/', views.UserManagementView.as_view(), name='users'),
    path('users/<int:pk>/toggle-active/', views.UserToggleActiveView.as_view(), name='toggle_user_active'),
    
    # Inquiry Management
    path('inquiries/', views.InquiryManagementView.as_view(), name='inquiries'),
    
    # Service Requests
    path('services/', views.ServiceRequestsView.as_view(), name='services'),
    
    # Analytics
    path('analytics/', views.AnalyticsView.as_view(), name='analytics'),
    path('api/stats/', views.ApiStatsView.as_view(), name='api_stats'),
]
