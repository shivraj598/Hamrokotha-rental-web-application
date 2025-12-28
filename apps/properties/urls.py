"""
Properties app URL configuration.
"""

from django.urls import path
from . import views

app_name = 'properties'

urlpatterns = [
    # Property listings
    path('', views.PropertyListView.as_view(), name='list'),
    path('search/', views.PropertySearchView.as_view(), name='search'),
    path('<int:pk>/', views.PropertyDetailView.as_view(), name='detail'),
    
    # Landlord property management
    path('add/', views.PropertyCreateView.as_view(), name='add'),
    path('<int:pk>/edit/', views.PropertyUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.PropertyDeleteView.as_view(), name='delete'),
    path('<int:pk>/mark-rented/', views.MarkAsRentedView.as_view(), name='mark_rented'),
    
    # Favorites
    path('favorites/', views.FavoritesListView.as_view(), name='favorites'),
    path('<int:pk>/favorite/', views.ToggleFavoriteView.as_view(), name='toggle_favorite'),
    
    # API endpoints
    path('api/areas/<str:district>/', views.AreasAPIView.as_view(), name='api_areas'),
]
