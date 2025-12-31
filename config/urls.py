"""
URL configuration for HamroKotha Rental Platform.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),
    
    # Core app (homepage, etc.)
    path('', include('apps.core.urls', namespace='core')),
    
    # User Authentication & Profiles
    path('', include('apps.accounts.urls', namespace='accounts')),
    
    # Property Management
    path('properties/', include('apps.properties.urls', namespace='properties')),
    
    # Inquiries
    path('inquiries/', include('apps.inquiries.urls', namespace='inquiries')),
    
    # Services (Find Room, Shift Home)
    path('services/', include('apps.services.urls', namespace='services')),
    
    # Custom Admin Panel
    path('admin-dashboard/', include('apps.admin_panel.urls', namespace='admin_panel')),
    
    # Chat
    path('chat/', include('apps.chat.urls', namespace='chat')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    # Debug Toolbar (disabled to avoid redirect interception issues)
    # import debug_toolbar
    # urlpatterns = [
    #     path('__debug__/', include(debug_toolbar.urls)),
    # ] + urlpatterns

# Custom admin site configuration
admin.site.site_header = 'HamroKotha Administration'
admin.site.site_title = 'HamroKotha Admin'
admin.site.index_title = 'Welcome to HamroKotha Admin Panel'
