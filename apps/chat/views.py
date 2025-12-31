"""
Chat views for real-time messaging between landlords and tenants.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.db.models import Q, Max, Count
from django.utils import timezone
from django.contrib import messages

from .models import ChatRoom, Message
from apps.properties.models import Property
from apps.accounts.models import User


class ChatListView(LoginRequiredMixin, ListView):
    """List all chat rooms for the current user."""
    model = ChatRoom
    template_name = 'chat/chat_list.html'
    context_object_name = 'chat_rooms'
    
    def get_queryset(self):
        user = self.request.user
        return ChatRoom.objects.filter(
            Q(participant1=user) | Q(participant2=user),
            is_active=True
        ).select_related(
            'participant1', 'participant2', 'property'
        ).prefetch_related('messages').annotate(
            last_message_time=Max('messages__created_at')
        ).order_by('-last_message_time', '-updated_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Add unread counts for each chat room
        for room in context['chat_rooms']:
            room.unread_count = room.get_unread_count(user)
            room.other_user = room.get_other_participant(user)
            room.last_message = room.get_last_message()
        
        # Total unread count
        context['total_unread'] = sum(room.unread_count for room in context['chat_rooms'])
        
        return context


class ChatRoomView(LoginRequiredMixin, DetailView):
    """View a specific chat room and its messages."""
    model = ChatRoom
    template_name = 'chat/chat_room.html'
    context_object_name = 'chat_room'
    
    def get_queryset(self):
        user = self.request.user
        return ChatRoom.objects.filter(
            Q(participant1=user) | Q(participant2=user)
        ).select_related('participant1', 'participant2', 'property')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        room = self.object
        
        # Get messages
        context['messages_list'] = room.messages.select_related('sender').order_by('created_at')
        
        # Other participant
        context['other_user'] = room.get_other_participant(user)
        
        # Mark messages as read
        room.messages.filter(is_read=False).exclude(sender=user).update(
            is_read=True, 
            read_at=timezone.now()
        )
        
        return context


class StartChatView(LoginRequiredMixin, View):
    """Start a new chat or redirect to existing chat."""
    
    def get(self, request, user_id, property_id=None):
        other_user = get_object_or_404(User, pk=user_id)
        
        # Can't chat with yourself
        if other_user == request.user:
            messages.error(request, "You cannot chat with yourself.")
            return redirect('chat:list')
        
        # Get property if provided
        property_obj = None
        if property_id:
            property_obj = get_object_or_404(Property, pk=property_id)
        
        # Get or create chat room
        room, created = ChatRoom.get_or_create_room(
            request.user, 
            other_user, 
            property_obj
        )
        
        if created:
            messages.success(request, f"Chat started with {other_user.get_full_name()}")
        
        return redirect('chat:room', pk=room.pk)


class SendMessageView(LoginRequiredMixin, View):
    """Send a message in a chat room (AJAX)."""
    
    def post(self, request, pk):
        room = get_object_or_404(
            ChatRoom.objects.filter(
                Q(participant1=request.user) | Q(participant2=request.user)
            ),
            pk=pk
        )
        
        content = request.POST.get('content', '').strip()
        
        if not content:
            return JsonResponse({'success': False, 'error': 'Message cannot be empty'})
        
        # Create message
        message = Message.objects.create(
            chat_room=room,
            sender=request.user,
            content=content
        )
        
        # Update room timestamp
        room.save()  # This updates updated_at
        
        return JsonResponse({
            'success': True,
            'message': {
                'id': str(message.id),
                'content': message.content,
                'sender_id': message.sender.id,
                'sender_name': message.sender.get_full_name(),
                'created_at': message.created_at.strftime('%I:%M %p'),
                'is_own': True
            }
        })


class GetMessagesView(LoginRequiredMixin, View):
    """Get new messages for polling (AJAX)."""
    
    def get(self, request, pk):
        room = get_object_or_404(
            ChatRoom.objects.filter(
                Q(participant1=request.user) | Q(participant2=request.user)
            ),
            pk=pk
        )
        
        # Get messages after a certain ID
        after_id = request.GET.get('after')
        
        messages_qs = room.messages.select_related('sender').order_by('created_at')
        
        if after_id:
            try:
                last_message = Message.objects.get(pk=after_id)
                messages_qs = messages_qs.filter(created_at__gt=last_message.created_at)
            except Message.DoesNotExist:
                pass
        
        # Mark messages from other user as read
        messages_qs.filter(is_read=False).exclude(sender=request.user).update(
            is_read=True,
            read_at=timezone.now()
        )
        
        messages_data = []
        for msg in messages_qs:
            messages_data.append({
                'id': str(msg.id),
                'content': msg.content,
                'sender_id': msg.sender.id,
                'sender_name': msg.sender.get_full_name(),
                'sender_initial': msg.sender.first_name[:1].upper() if msg.sender.first_name else msg.sender.username[:1].upper(),
                'created_at': msg.created_at.strftime('%I:%M %p'),
                'is_own': msg.sender == request.user
            })
        
        return JsonResponse({
            'success': True,
            'messages': messages_data
        })


class GetUnreadCountView(LoginRequiredMixin, View):
    """Get total unread message count (AJAX for navbar badge)."""
    
    def get(self, request):
        user = request.user
        
        # Count unread messages across all chat rooms
        unread_count = Message.objects.filter(
            Q(chat_room__participant1=user) | Q(chat_room__participant2=user),
            is_read=False
        ).exclude(sender=user).count()
        
        return JsonResponse({
            'success': True,
            'unread_count': unread_count
        })
