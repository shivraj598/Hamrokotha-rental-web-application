"""
Property views for listing, creating, and managing properties.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, View
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.utils import timezone

from .models import Property, PropertyImage, Favorite, PropertyView
from .forms import PropertyForm, PropertyImageFormSet, PropertyFilterForm
from apps.core.choices import PropertyStatus


class PropertyListView(ListView):
    """Public property listing with filters."""
    model = Property
    template_name = 'properties/list.html'
    context_object_name = 'properties'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Property.objects.filter(
            status=PropertyStatus.APPROVED
        ).select_related('owner').prefetch_related('images')
        
        # Search query
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q) |
                Q(area__icontains=q) |
                Q(address__icontains=q)
            )
        
        # Filter by district (case-insensitive)
        district = self.request.GET.get('district')
        if district:
            queryset = queryset.filter(district__iexact=district)
        
        # Filter by property type (case-insensitive)
        property_type = self.request.GET.get('property_type')
        if property_type:
            queryset = queryset.filter(property_type__iexact=property_type)
        
        # Filter by price range
        min_price = self.request.GET.get('min_price')
        if min_price:
            queryset = queryset.filter(price_per_month__gte=min_price)
        
        max_price = self.request.GET.get('max_price')
        if max_price:
            queryset = queryset.filter(price_per_month__lte=max_price)
        
        # Filter by bedrooms
        bedrooms = self.request.GET.get('bedrooms')
        if bedrooms:
            queryset = queryset.filter(bedrooms__gte=int(bedrooms))
        
        # Filter by area
        area = self.request.GET.get('area')
        if area:
            queryset = queryset.filter(area__icontains=area)
        
        # Sorting
        sort = self.request.GET.get('sort', '-created_at')
        valid_sort_options = [
            '-created_at', 'created_at', 
            'price_per_month', '-price_per_month',
            '-views_count'
        ]
        if sort in valid_sort_options:
            queryset = queryset.order_by(sort)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = PropertyFilterForm(self.request.GET)
        context['total_count'] = self.get_queryset().count()
        
        # User favorites for marking
        if self.request.user.is_authenticated:
            context['user_favorites'] = set(
                Favorite.objects.filter(
                    user=self.request.user
                ).values_list('property_id', flat=True)
            )
        
        return context


class PropertyDetailView(DetailView):
    """Property detail view."""
    model = Property
    template_name = 'properties/detail.html'
    context_object_name = 'property'
    
    def get_queryset(self):
        # Show approved properties to everyone, owner can see their own
        queryset = Property.objects.select_related('owner').prefetch_related('images')
        if self.request.user.is_authenticated:
            return queryset.filter(
                Q(status=PropertyStatus.APPROVED) |
                Q(owner=self.request.user)
            )
        return queryset.filter(status=PropertyStatus.APPROVED)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        property_obj = self.object
        
        # Check if favorited
        if self.request.user.is_authenticated:
            context['is_favorited'] = Favorite.objects.filter(
                user=self.request.user,
                property=property_obj
            ).exists()
        
        # Related properties (same district, different property)
        context['related_properties'] = Property.objects.filter(
            status=PropertyStatus.APPROVED,
            district=property_obj.district
        ).exclude(pk=property_obj.pk).order_by('-created_at')[:4]
        
        return context
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        
        # Record property view (don't count owner's views)
        property_obj = self.object
        if not request.user.is_authenticated or request.user != property_obj.owner:
            # Increment view count
            property_obj.increment_views()
            
            # Log view for analytics
            PropertyView.objects.create(
                property=property_obj,
                user=request.user if request.user.is_authenticated else None,
                ip_address=self.get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
        
        return response
    
    def get_client_ip(self, request):
        """Get client IP address."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')


class LandlordRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Mixin to ensure user is a landlord (not admin). Admins can only approve/reject, not create."""
    
    def test_func(self):
        # Only landlords can create/edit properties, NOT admins
        return self.request.user.is_landlord and not (self.request.user.is_staff or self.request.user.is_superuser)
    
    def handle_no_permission(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            messages.error(self.request, "Admins cannot create properties. You can only approve or reject listings.")
        else:
            messages.error(self.request, "Only landlords can perform this action.")
        return redirect('accounts:dashboard')


class PropertyCreateView(LandlordRequiredMixin, SuccessMessageMixin, CreateView):
    """Create new property listing."""
    model = Property
    form_class = PropertyForm
    template_name = 'properties/create.html'
    success_message = "Property submitted for review! It will be visible once approved."
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['image_formset'] = PropertyImageFormSet(
                self.request.POST, 
                self.request.FILES
            )
        else:
            context['image_formset'] = PropertyImageFormSet()
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context['image_formset']
        
        if image_formset.is_valid():
            form.instance.owner = self.request.user
            form.instance.status = PropertyStatus.PENDING
            self.object = form.save()
            
            image_formset.instance = self.object
            image_formset.save()
            
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))
    
    def get_success_url(self):
        return reverse_lazy('accounts:dashboard')


class PropertyOwnerMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Mixin to ensure user owns the property or is admin."""
    
    def test_func(self):
        property_obj = self.get_object()
        user = self.request.user
        return user == property_obj.owner or user.is_staff or user.is_superuser
    
    def handle_no_permission(self):
        messages.error(self.request, "You don't have permission to edit this property.")
        return redirect('properties:list')


class PropertyUpdateView(PropertyOwnerMixin, SuccessMessageMixin, UpdateView):
    """Edit property listing."""
    model = Property
    form_class = PropertyForm
    template_name = 'properties/edit.html'
    success_message = "Property updated successfully!"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['image_formset'] = PropertyImageFormSet(
                self.request.POST,
                self.request.FILES,
                instance=self.object
            )
        else:
            context['image_formset'] = PropertyImageFormSet(instance=self.object)
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context['image_formset']
        
        if image_formset.is_valid():
            # Reset to pending if major changes
            if form.has_changed():
                form.instance.status = PropertyStatus.PENDING
                messages.info(
                    self.request, 
                    "Your property has been resubmitted for review due to changes."
                )
            
            self.object = form.save()
            image_formset.save()
            
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))
    
    def get_success_url(self):
        return reverse_lazy('properties:detail', kwargs={'pk': self.object.pk})


class PropertyDeleteView(PropertyOwnerMixin, DeleteView):
    """Delete property listing."""
    model = Property
    template_name = 'properties/delete.html'
    success_url = reverse_lazy('accounts:dashboard')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, "Property deleted successfully.")
        return super().delete(request, *args, **kwargs)


class ToggleFavoriteView(LoginRequiredMixin, View):
    """Toggle favorite status for a property."""
    
    def post(self, request, pk):
        property_obj = get_object_or_404(Property, pk=pk)
        
        favorite, created = Favorite.objects.get_or_create(
            user=request.user,
            property=property_obj
        )
        
        if not created:
            favorite.delete()
            is_favorited = False
            message = "Property removed from favorites"
        else:
            is_favorited = True
            message = "Property added to favorites"
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'is_favorited': is_favorited,
                'message': message
            })
        
        messages.success(request, message)
        return redirect(request.META.get('HTTP_REFERER', 'properties:list'))


class FavoriteListView(LoginRequiredMixin, ListView):
    """List user's favorite properties."""
    template_name = 'properties/favorites.html'
    context_object_name = 'favorites'
    paginate_by = 12
    
    def get_queryset(self):
        return Favorite.objects.filter(
            user=self.request.user
        ).select_related('property', 'property__owner').prefetch_related('property__images')


class MyPropertiesView(LandlordRequiredMixin, ListView):
    """List landlord's own properties."""
    template_name = 'properties/my_properties.html'
    context_object_name = 'properties'
    paginate_by = 12
    
    def get_queryset(self):
        return Property.objects.filter(
            owner=self.request.user
        ).prefetch_related('images').order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        properties = self.get_queryset()
        
        context['total_properties'] = properties.count()
        context['pending_count'] = properties.filter(status=PropertyStatus.PENDING).count()
        context['approved_count'] = properties.filter(status=PropertyStatus.APPROVED).count()
        context['rented_count'] = properties.filter(status=PropertyStatus.RENTED).count()
        context['rejected_count'] = properties.filter(status=PropertyStatus.REJECTED).count()
        
        return context


class MarkAsRentedView(PropertyOwnerMixin, View):
    """Mark a property as rented."""
    
    def post(self, request, pk):
        property_obj = self.get_object()
        property_obj.status = PropertyStatus.RENTED
        property_obj.save()
        
        messages.success(request, "Property marked as rented.")
        return redirect('properties:my_properties')
    
    def get_object(self):
        return get_object_or_404(Property, pk=self.kwargs['pk'])


class MarkAsAvailableView(PropertyOwnerMixin, View):
    """Mark a rented property as available again."""
    
    def post(self, request, pk):
        property_obj = self.get_object()
        property_obj.status = PropertyStatus.APPROVED
        property_obj.save()
        
        messages.success(request, "Property marked as available.")
        return redirect('properties:my_properties')
    
    def get_object(self):
        return get_object_or_404(Property, pk=self.kwargs['pk'])
