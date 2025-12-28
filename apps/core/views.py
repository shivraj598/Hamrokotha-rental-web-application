"""
Core app views - Homepage and static pages.
"""

from django.views.generic import TemplateView
from django.db.models import Count


class HomeView(TemplateView):
    """Homepage with featured properties and search."""
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Import here to avoid circular imports
        from apps.properties.models import Property
        from apps.core.choices import PropertyStatus, District
        
        # Featured/Recent properties (approved only)
        context['featured_properties'] = Property.objects.filter(
            status=PropertyStatus.APPROVED
        ).select_related('owner').prefetch_related('images').order_by('-created_at')[:6]
        
        # Property statistics
        context['total_properties'] = Property.objects.filter(
            status=PropertyStatus.APPROVED
        ).count()
        
        # Properties by district
        context['properties_by_district'] = Property.objects.filter(
            status=PropertyStatus.APPROVED
        ).values('district').annotate(count=Count('id'))
        
        context['districts'] = District.choices
        
        return context


class AboutView(TemplateView):
    """About us page."""
    template_name = 'pages/about.html'


class ContactView(TemplateView):
    """Contact page."""
    template_name = 'pages/contact.html'


class PrivacyPolicyView(TemplateView):
    """Privacy policy page."""
    template_name = 'pages/privacy.html'


class TermsView(TemplateView):
    """Terms of service page."""
    template_name = 'pages/terms.html'
