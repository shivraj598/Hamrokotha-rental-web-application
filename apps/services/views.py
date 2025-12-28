from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy

from .models import FindRoomRequest, ShiftHomeRequest
from .forms import FindRoomRequestForm, ShiftHomeRequestForm


class ServicesHomeView(TemplateView):
    """Services landing page."""
    template_name = 'services/home.html'


# Find Room Views
class FindRoomCreateView(LoginRequiredMixin, CreateView):
    """Create a Find Room request."""
    model = FindRoomRequest
    form_class = FindRoomRequestForm
    template_name = 'services/find_room/create.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()
        messages.success(
            self.request, 
            "Your room finding request has been submitted! We'll get back to you soon."
        )
        return redirect('services:find_room_success', pk=self.object.pk)


class FindRoomSuccessView(LoginRequiredMixin, DetailView):
    """Success page after Find Room request submission."""
    model = FindRoomRequest
    template_name = 'services/find_room/success.html'
    context_object_name = 'request_obj'
    
    def get_queryset(self):
        return FindRoomRequest.objects.filter(user=self.request.user)


class FindRoomListView(LoginRequiredMixin, ListView):
    """List user's Find Room requests."""
    model = FindRoomRequest
    template_name = 'services/find_room/list.html'
    context_object_name = 'requests'
    paginate_by = 10
    
    def get_queryset(self):
        return FindRoomRequest.objects.filter(user=self.request.user)


class FindRoomDetailView(LoginRequiredMixin, DetailView):
    """View Find Room request details."""
    model = FindRoomRequest
    template_name = 'services/find_room/detail.html'
    context_object_name = 'request_obj'
    
    def get_queryset(self):
        return FindRoomRequest.objects.filter(user=self.request.user)


# Shift Home Views
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
            "Your home shifting request has been submitted! We'll contact you with a quote soon."
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
