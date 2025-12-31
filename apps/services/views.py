from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse

from .models import FindRoomRequest, ShiftHomeRequest, RoomRequestReply
from .forms import FindRoomRequestForm, ShiftHomeRequestForm, RoomRequestReplyForm


class ServicesHomeView(TemplateView):
    """Services landing page."""
    template_name = 'services/home.html'


# ============== Find Room Views ==============

class FindRoomCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Create a Find Room request - only for tenants."""
    model = FindRoomRequest
    form_class = FindRoomRequestForm
    template_name = 'services/find_room/create.html'
    
    def test_func(self):
        return self.request.user.user_type == 'TENANT'
    
    def handle_no_permission(self):
        messages.error(self.request, "Only tenants can post room requests.")
        return redirect('core:home')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()
        messages.success(
            self.request, 
            "Your room request has been posted! Landlords can now see and reply to your request."
        )
        return redirect('services:room_request_detail', pk=self.object.pk)


class RoomRequestListView(ListView):
    """List all active room requests - social feed style for landlords."""
    model = FindRoomRequest
    template_name = 'services/find_room/feed.html'
    context_object_name = 'requests'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = FindRoomRequest.objects.filter(status='ACTIVE')
        
        # Filter by district
        district = self.request.GET.get('district')
        if district:
            queryset = queryset.filter(district=district)
        
        # Filter by property type
        property_type = self.request.GET.get('property_type')
        if property_type:
            queryset = queryset.filter(property_type=property_type)
        
        # Filter by budget
        budget = self.request.GET.get('budget')
        if budget:
            queryset = queryset.filter(budget_range=budget)
        
        return queryset.select_related('user')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['districts'] = FindRoomRequest.DISTRICT_CHOICES
        context['property_types'] = FindRoomRequest.PROPERTY_TYPES
        context['budget_ranges'] = FindRoomRequest.BUDGET_CHOICES
        return context


class RoomRequestDetailView(DetailView):
    """View room request details with replies - Twitter-style post detail."""
    model = FindRoomRequest
    template_name = 'services/find_room/post_detail.html'
    context_object_name = 'request_obj'
    
    def get_queryset(self):
        return FindRoomRequest.objects.select_related('user').prefetch_related(
            'replies__landlord', 'replies__property_link__images'
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Increment view count
        if user.is_authenticated and user != self.object.user:
            self.object.views_count += 1
            self.object.save(update_fields=['views_count'])
        
        # Add reply form for landlords
        if user.is_authenticated and user.user_type == 'LANDLORD':
            context['reply_form'] = RoomRequestReplyForm(landlord=user)
            context['can_reply'] = True
        
        # Check if current user is the owner
        context['is_owner'] = user.is_authenticated and user == self.object.user
        
        return context


class RoomRequestReplyView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Handle reply submission from landlords."""
    
    def test_func(self):
        return self.request.user.user_type == 'LANDLORD'
    
    def post(self, request, pk):
        room_request = get_object_or_404(FindRoomRequest, pk=pk)
        form = RoomRequestReplyForm(request.POST, landlord=request.user)
        
        if form.is_valid():
            reply = form.save(commit=False)
            reply.room_request = room_request
            reply.landlord = request.user
            reply.save()
            messages.success(request, "Your reply has been posted!")
        else:
            messages.error(request, "Failed to post reply. Please check your input.")
        
        return redirect('services:room_request_detail', pk=pk)


class MyRoomRequestsView(LoginRequiredMixin, ListView):
    """List current user's room requests."""
    model = FindRoomRequest
    template_name = 'services/find_room/my_requests.html'
    context_object_name = 'requests'
    paginate_by = 10
    
    def get_queryset(self):
        return FindRoomRequest.objects.filter(user=self.request.user)


class CloseRoomRequestView(LoginRequiredMixin, View):
    """Close a room request."""
    
    def post(self, request, pk):
        room_request = get_object_or_404(FindRoomRequest, pk=pk, user=request.user)
        room_request.status = 'CLOSED'
        room_request.save()
        messages.success(request, "Your room request has been closed.")
        return redirect('services:my_room_requests')


class DeleteRoomRequestView(LoginRequiredMixin, View):
    """Delete a room request."""
    
    def post(self, request, pk):
        room_request = get_object_or_404(FindRoomRequest, pk=pk, user=request.user)
        room_request.delete()
        messages.success(request, "Your room request has been deleted.")
        return redirect('services:my_room_requests')


# ============== Shift Home Views ==============

class ShiftHomeCreateView(LoginRequiredMixin, CreateView):
    """Create a Shift Home request."""
    model = ShiftHomeRequest
    form_class = ShiftHomeRequestForm
    template_name = 'services/shift_home/create.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()
        messages.success(
            self.request, 
            "Your home shifting request has been submitted! Our team will contact you soon."
        )
        return redirect('services:shift_home_success', pk=self.object.pk)


class ShiftHomeSuccessView(LoginRequiredMixin, DetailView):
    """Success page after Shift Home request submission."""
    model = ShiftHomeRequest
    template_name = 'services/shift_home/success.html'
    context_object_name = 'request_obj'
    
    def get_queryset(self):
        return ShiftHomeRequest.objects.filter(user=self.request.user)


class ShiftHomeListView(LoginRequiredMixin, ListView):
    """List user's Shift Home requests."""
    model = ShiftHomeRequest
    template_name = 'services/shift_home/list.html'
    context_object_name = 'requests'
    paginate_by = 10
    
    def get_queryset(self):
        return ShiftHomeRequest.objects.filter(user=self.request.user)


class ShiftHomeDetailView(LoginRequiredMixin, DetailView):
    """View Shift Home request details."""
    model = ShiftHomeRequest
    template_name = 'services/shift_home/detail.html'
    context_object_name = 'request_obj'
    
    def get_queryset(self):
        return ShiftHomeRequest.objects.filter(user=self.request.user)


class DeleteShiftHomeRequestView(LoginRequiredMixin, View):
    """Delete a shift home request."""
    
    def post(self, request, pk):
        shift_request = get_object_or_404(ShiftHomeRequest, pk=pk, user=request.user)
        shift_request.delete()
        messages.success(request, "Your shift home request has been deleted.")
        return redirect('services:shift_home_list')


# Legacy views for compatibility
FindRoomSuccessView = RoomRequestDetailView
FindRoomListView = MyRoomRequestsView
FindRoomDetailView = RoomRequestDetailView
