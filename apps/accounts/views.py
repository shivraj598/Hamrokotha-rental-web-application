"""
User authentication and profile views.
"""

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordResetView, 
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from .forms import (
    LandlordRegistrationForm, TenantRegistrationForm, 
    CustomLoginForm, CustomPasswordResetForm, UserProfileForm
)
from apps.core.choices import PropertyStatus


class RegisterView(TemplateView):
    """Registration type selection page."""
    template_name = 'accounts/register.html'


class LandlordRegisterView(SuccessMessageMixin, CreateView):
    """Landlord registration view."""
    template_name = 'accounts/register_landlord.html'
    form_class = LandlordRegistrationForm
    success_url = reverse_lazy('accounts:login')
    success_message = "Account created successfully! Please log in."
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('accounts:dashboard')
        return super().dispatch(request, *args, **kwargs)


class TenantRegisterView(SuccessMessageMixin, CreateView):
    """Tenant registration view."""
    template_name = 'accounts/register_tenant.html'
    form_class = TenantRegistrationForm
    success_url = reverse_lazy('accounts:login')
    success_message = "Account created successfully! Please log in."
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('accounts:dashboard')
        return super().dispatch(request, *args, **kwargs)


class CustomLoginView(LoginView):
    """Custom login view."""
    template_name = 'accounts/login.html'
    form_class = CustomLoginForm
    redirect_authenticated_user = True
    
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse_lazy('accounts:dashboard')
    
    def form_valid(self, form):
        user = form.get_user()
        if user.is_banned:
            messages.error(self.request, f"Your account has been banned. Reason: {user.ban_reason or 'No reason provided'}")
            return redirect('accounts:login')
        messages.success(self.request, f"Welcome back, {user.get_full_name() or user.username}!")
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    """Custom logout view."""
    next_page = reverse_lazy('core:home')
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.success(request, "You have been logged out successfully.")
        return super().dispatch(request, *args, **kwargs)


class CustomPasswordResetView(PasswordResetView):
    """Custom password reset view."""
    template_name = 'accounts/password_reset.html'
    form_class = CustomPasswordResetForm
    email_template_name = 'accounts/email/password_reset_email.html'
    subject_template_name = 'accounts/email/password_reset_subject.txt'
    success_url = reverse_lazy('accounts:password_reset_done')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    """Password reset done view."""
    template_name = 'accounts/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """Password reset confirm view."""
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    """Password reset complete view."""
    template_name = 'accounts/password_reset_complete.html'


class ProfileView(LoginRequiredMixin, TemplateView):
    """User profile view."""
    template_name = 'accounts/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        if user.is_landlord:
            from apps.properties.models import Property
            context['properties'] = Property.objects.filter(owner=user).order_by('-created_at')[:5]
            context['total_properties'] = Property.objects.filter(owner=user).count()
            context['approved_properties'] = Property.objects.filter(
                owner=user, status=PropertyStatus.APPROVED
            ).count()
        
        if user.is_tenant:
            from apps.properties.models import Favorite
            context['favorites'] = Favorite.objects.filter(user=user).select_related('property')[:5]
            context['total_favorites'] = Favorite.objects.filter(user=user).count()
        
        return context


class ProfileEditView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Edit user profile view."""
    template_name = 'accounts/profile_edit.html'
    form_class = UserProfileForm
    success_url = reverse_lazy('accounts:profile')
    success_message = "Profile updated successfully!"
    
    def get_object(self):
        return self.request.user


class DashboardView(LoginRequiredMixin, TemplateView):
    """User dashboard view - different content based on user type."""
    template_name = 'accounts/dashboard.html'
    
    def get_template_names(self):
        user = self.request.user
        if user.is_landlord:
            return ['accounts/dashboard_landlord.html']
        elif user.is_tenant:
            return ['accounts/dashboard_tenant.html']
        return ['accounts/dashboard.html']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        if user.is_landlord:
            from apps.properties.models import Property
            from apps.inquiries.models import Inquiry
            
            # Landlord's properties
            properties = Property.objects.filter(owner=user)
            context['properties'] = properties.order_by('-created_at')
            context['total_properties'] = properties.count()
            context['pending_properties'] = properties.filter(status=PropertyStatus.PENDING).count()
            context['approved_properties'] = properties.filter(status=PropertyStatus.APPROVED).count()
            context['rented_properties'] = properties.filter(status=PropertyStatus.RENTED).count()
            
            # Inquiries received
            context['recent_inquiries'] = Inquiry.objects.filter(
                rental_property__owner=user
            ).select_related('rental_property', 'tenant').order_by('-created_at')[:5]
            context['total_inquiries'] = Inquiry.objects.filter(rental_property__owner=user).count()
            context['pending_inquiries'] = Inquiry.objects.filter(
                rental_property__owner=user, status='PENDING'
            ).count()
            
            # Total views
            context['total_views'] = sum(p.views_count for p in properties)
        
        elif user.is_tenant:
            from apps.properties.models import Property, Favorite
            from apps.inquiries.models import Inquiry
            
            # Favorite properties
            context['favorites'] = Favorite.objects.filter(
                user=user
            ).select_related('property').order_by('-created_at')[:6]
            context['total_favorites'] = Favorite.objects.filter(user=user).count()
            
            # Inquiries sent
            context['inquiries'] = Inquiry.objects.filter(
                tenant=user
            ).select_related('property').order_by('-created_at')[:5]
            context['total_inquiries'] = Inquiry.objects.filter(tenant=user).count()
            
            # Recommended properties
            context['recommended_properties'] = Property.objects.filter(
                status=PropertyStatus.APPROVED
            ).order_by('-created_at')[:6]
        
        return context
