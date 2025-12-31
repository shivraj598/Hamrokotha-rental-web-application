"""
Chat models for real-time messaging between landlords and tenants.
"""

import uuid
from django.db import models
from django.conf import settings
from apps.properties.models import Property


class ChatRoom(models.Model):
    """
    Chat room between two users, optionally linked to a property.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Participants
    participant1 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='chat_rooms_as_participant1'
    )
    participant2 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='chat_rooms_as_participant2'
    )
    
    # Optional property link (for context)
    property = models.ForeignKey(
        Property,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='chat_rooms'
    )
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'Chat Room'
        verbose_name_plural = 'Chat Rooms'
    
    def __str__(self):
        return f"Chat: {self.participant1.get_full_name()} & {self.participant2.get_full_name()}"
    
    def get_other_participant(self, user):
        """Get the other participant in the chat."""
        if user == self.participant1:
            return self.participant2
        return self.participant1
    
    def get_last_message(self):
        """Get the most recent message in this chat."""
        return self.messages.order_by('-created_at').first()
    
    def get_unread_count(self, user):
        """Get count of unread messages for a user."""
        return self.messages.filter(is_read=False).exclude(sender=user).count()
    
    @classmethod
    def get_or_create_room(cls, user1, user2, property_obj=None):
        """
        Get existing chat room between two users or create a new one.
        """
        # Check both orderings
        room = cls.objects.filter(
            models.Q(participant1=user1, participant2=user2) |
            models.Q(participant1=user2, participant2=user1)
        ).first()
        
        if room:
            # Update property if provided and room doesn't have one
            if property_obj and not room.property:
                room.property = property_obj
                room.save()
            return room, False
        
        # Create new room
        room = cls.objects.create(
            participant1=user1,
            participant2=user2,
            property=property_obj
        )
        return room, True


class Message(models.Model):
    """
    Individual message in a chat room.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    chat_room = models.ForeignKey(
        ChatRoom,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    
    # Message content
    content = models.TextField()
    
    # Status
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
    
    def __str__(self):
        return f"{self.sender.get_full_name()}: {self.content[:50]}"
    
    def mark_as_read(self):
        """Mark message as read."""
        if not self.is_read:
            from django.utils import timezone
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])
