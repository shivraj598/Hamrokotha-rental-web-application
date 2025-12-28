"""
Inquiries app URL configuration.
"""

from django.urls import path
from . import views

app_name = 'inquiries'

urlpatterns = [
    # Inquiry management
    path('', views.InquiryListView.as_view(), name='list'),
    path('send/<int:property_id>/', views.SendInquiryView.as_view(), name='send'),
    path('<int:pk>/', views.InquiryDetailView.as_view(), name='detail'),
    path('<int:pk>/reply/', views.InquiryReplyView.as_view(), name='reply'),
    path('<int:pk>/close/', views.CloseInquiryView.as_view(), name='close'),
]
