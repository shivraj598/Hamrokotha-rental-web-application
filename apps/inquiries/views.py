from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.db.models import Q, Count
from django.urls import reverse

from apps.properties.models import Property
from .models import Inquiry, InquiryMessage
from .forms import InquiryForm, InquiryMessageForm


class InquiryCreateView(LoginRequiredMixin, CreateView):
    """Create a new inquiry for a property."""
    model = Inquiry
    form_class = InquiryForm
    template_name = 'inquiries/create.html'
    
    def get_property(self):
        return get_object_or_404(Property, pk=self.kwargs['property_pk'], status='APPROVED')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['property'] = self.get_property()
        return context
    
    def form_valid(self, form):
        property_obj = self.get_property()
        
        # Check if user is the owner
        if property_obj.owner == self.request.user:
            messages.error(self.request, "You cannot send an inquiry for your own property.")
            return redirect('properties:detail', pk=property_obj.pk)
        
        # Check if user already has an active inquiry for this property
        existing_inquiry = Inquiry.objects.filter(
            rental_property=property_obj,
            sender=self.request.user,
            status__in=['PENDING', 'RESPONDED']
        ).first()
        
        if existing_inquiry:
            messages.info(self.request, "You already have an active inquiry for this property.")
            return redirect('inquiries:detail', pk=existing_inquiry.pk)
        
        form.instance.rental_property = property_obj
        form.instance.sender = self.request.user
        self.object = form.save()
        
        messages.success(self.request, "Your inquiry has been sent successfully! The landlord will respond soon.")
        return redirect('inquiries:detail', pk=self.object.pk)


class InquiryListView(LoginRequiredMixin, ListView):
    """List inquiries for landlord or tenant."""
    model = Inquiry
    template_name = 'inquiries/list.html'
    context_object_name = 'inquiries'
    paginate_by = 10
    
    def get_queryset(self):
        user = self.request.user
        
        # Admin/staff see all inquiries
        if user.is_staff or user.is_superuser:
            queryset = Inquiry.objects.all()
        # Landlords see inquiries on their properties
        elif user.user_type == 'LANDLORD':
            queryset = Inquiry.objects.filter(rental_property__owner=user)
        # Tenants see their sent inquiries
        else:
            queryset = Inquiry.objects.filter(sender=user)
        
        # Apply filters (case-insensitive)
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status__iexact=status)
        
        read_status = self.request.GET.get('read_status')
        if read_status == 'unread':
            queryset = queryset.filter(is_read=False)
        elif read_status == 'read':
            queryset = queryset.filter(is_read=True)
        
        property_id = self.request.GET.get('property_id')
        if property_id:
            queryset = queryset.filter(rental_property_id=property_id)
        
        return queryset.select_related('rental_property', 'sender')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Admin/staff see stats for all inquiries
        if user.is_staff or user.is_superuser:
            base_qs = Inquiry.objects.all()
        elif user.user_type == 'LANDLORD':
            base_qs = Inquiry.objects.filter(rental_property__owner=user)
        else:
            base_qs = Inquiry.objects.filter(sender=user)
        
        context['total_inquiries'] = base_qs.count()
        context['pending_count'] = base_qs.filter(status='PENDING').count()
        context['responded_count'] = base_qs.filter(status='RESPONDED').count()
        context['closed_count'] = base_qs.filter(status='CLOSED').count()
        context['unread_count'] = base_qs.filter(is_read=False).count()
        
        return context


class InquiryDetailView(LoginRequiredMixin, DetailView):
    """View inquiry details and messages."""
    model = Inquiry
    template_name = 'inquiries/detail.html'
    context_object_name = 'inquiry'
    
    def get_queryset(self):
        user = self.request.user
        # Admin/staff can view all inquiries
        if user.is_staff or user.is_superuser:
            return Inquiry.objects.select_related('rental_property', 'sender', 'rental_property__owner')
        # User can view if they're the sender or the landlord
        return Inquiry.objects.filter(
            Q(sender=user) | Q(rental_property__owner=user)
        ).select_related('rental_property', 'sender', 'rental_property__owner')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages_list'] = self.object.messages.select_related('sender').all()
        
        user = self.request.user
        # Check if user can respond (only landlord and tenant can, not admin)
        is_landlord = user == self.object.rental_property.owner
        is_tenant = user == self.object.sender
        context['can_respond'] = is_landlord or is_tenant
        
        # Only show message form if user can respond
        if context['can_respond']:
            context['message_form'] = InquiryMessageForm()
        
        # Mark as read for landlord
        if is_landlord:
            self.object.mark_as_read()
            # Mark all messages from tenant as read
            self.object.messages.filter(sender=self.object.sender).update(is_read=True)
        elif is_tenant:
            # Mark all messages from landlord as read for tenant
            self.object.messages.filter(sender=self.object.rental_property.owner).update(is_read=True)
        # Admin just views, no marking as read
        
        return context


class InquirySendMessageView(LoginRequiredMixin, View):
    """Send a message in an inquiry thread."""
    
    def post(self, request, pk):
        inquiry = get_object_or_404(Inquiry, pk=pk)
        
        # Check permission
        if request.user != inquiry.sender and request.user != inquiry.rental_property.owner:
            return HttpResponseForbidden("You don't have permission to send messages in this inquiry.")
        
        form = InquiryMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.inquiry = inquiry
            message.sender = request.user
            message.save()
            
            # Update inquiry status
            if request.user == inquiry.rental_property.owner and inquiry.status == 'PENDING':
                inquiry.status = 'RESPONDED'
                inquiry.save(update_fields=['status'])
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': {
                        'sender': request.user.get_full_name(),
                        'text': message.message,
                        'created_at': message.created_at.strftime('%b %d, %Y %I:%M %p'),
                        'is_own': True,
                    }
                })
            
            messages.success(request, "Your message has been sent.")
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)
            messages.error(request, "There was an error sending your message.")
        
        return redirect('inquiries:detail', pk=inquiry.pk)


class InquiryCloseView(LoginRequiredMixin, View):
    """Close an inquiry."""
    
    def post(self, request, pk):
        inquiry = get_object_or_404(Inquiry, pk=pk)
        
        # Only landlord can close inquiry
        if request.user != inquiry.rental_property.owner:
            return HttpResponseForbidden("Only the property owner can close this inquiry.")
        
        inquiry.status = 'CLOSED'
        inquiry.save(update_fields=['status'])
        
        messages.success(request, "Inquiry has been closed.")
        return redirect('inquiries:detail', pk=inquiry.pk)


class InquiryReopenView(LoginRequiredMixin, View):
    """Reopen a closed inquiry."""
    
    def post(self, request, pk):
        inquiry = get_object_or_404(Inquiry, pk=pk)
        
        # Both parties can reopen
        if request.user != inquiry.sender and request.user != inquiry.rental_property.owner:
            return HttpResponseForbidden("You don't have permission to reopen this inquiry.")
        
        inquiry.status = 'RESPONDED'
        inquiry.save(update_fields=['status'])
        
        messages.success(request, "Inquiry has been reopened.")
        return redirect('inquiries:detail', pk=inquiry.pk)


class UnreadCountView(LoginRequiredMixin, View):
    """Get unread inquiry count for navbar."""
    
    def get(self, request):
        user = request.user
        
        if user.user_type == 'LANDLORD':
            unread_count = Inquiry.objects.filter(
                rental_property__owner=user,
                is_read=False
            ).count()
            unread_messages = InquiryMessage.objects.filter(
                inquiry__rental_property__owner=user,
                is_read=False
            ).exclude(sender=user).count()
        else:
            unread_messages = InquiryMessage.objects.filter(
                inquiry__sender=user,
                is_read=False
            ).exclude(sender=user).count()
            unread_count = 0
        
        return JsonResponse({
            'unread_inquiries': unread_count,
            'unread_messages': unread_messages,
            'total': unread_count + unread_messages
        })
