from django.urls import path
from . import views

app_name = 'inquiries'

urlpatterns = [
    path('', views.InquiryListView.as_view(), name='list'),
    path('create/<uuid:property_pk>/', views.InquiryCreateView.as_view(), name='create'),
    path('<uuid:pk>/', views.InquiryDetailView.as_view(), name='detail'),
    path('<uuid:pk>/send-message/', views.InquirySendMessageView.as_view(), name='send_message'),
    path('<uuid:pk>/close/', views.InquiryCloseView.as_view(), name='close'),
    path('<uuid:pk>/reopen/', views.InquiryReopenView.as_view(), name='reopen'),
    path('unread-count/', views.UnreadCountView.as_view(), name='unread_count'),
]
