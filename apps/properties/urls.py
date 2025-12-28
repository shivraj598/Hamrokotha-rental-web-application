"""
Properties app URL configuration.
"""

from django.urls import path
from . import views

app_name = 'properties'

urlpatterns = [
    # Public views
    path('', views.PropertyListView.as_view(), name='list'),
    path('<uuid:pk>/', views.PropertyDetailView.as_view(), name='detail'),
    
    # Landlord views
    path('create/', views.PropertyCreateView.as_view(), name='create'),
    path('<uuid:pk>/edit/', views.PropertyUpdateView.as_view(), name='edit'),
    path('<uuid:pk>/delete/', views.PropertyDeleteView.as_view(), name='delete'),
    path('my-properties/', views.MyPropertiesView.as_view(), name='my_properties'),
    
    # Property status
    path('<uuid:pk>/mark-rented/', views.MarkAsRentedView.as_view(), name='mark_rented'),
    path('<uuid:pk>/mark-available/', views.MarkAsAvailableView.as_view(), name='mark_available'),
    
    # Favorites
    path('favorites/', views.FavoriteListView.as_view(), name='favorites'),
    path('<uuid:pk>/toggle-favorite/', views.ToggleFavoriteView.as_view(), name='toggle_favorite'),
]
