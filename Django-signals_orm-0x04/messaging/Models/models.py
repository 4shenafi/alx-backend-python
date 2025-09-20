# Task 4: Custom ORM Manager for Unread Messages
# This file demonstrates custom managers and advanced ORM techniques

import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


# Custom QuerySet for advanced message operations
class MessageQuerySet(models.QuerySet):
    """
    Custom QuerySet with advanced filtering and optimization methods.
    """
    def unread_only(self):
        """Filter only unread messages."""
        return self.filter(read=False)
    
    def for_user(self, user):
        """Filter messages for a specific user (received by them)."""
        return self.filter(receiver=user)
    
    def from_user(self, user):
        """Filter messages from a specific user (sent by them)."""
        return self.filter(sender=user)
    
    def recent(self, days=7):
        """Filter messages from the last N days."""
        from datetime import timedelta
        return self.filter(timestamp__gte=timezone.now() - timedelta(days=days))
    
    def with_sender_info(self):
        """Optimize query by selecting related sender information."""
        return self.select_related('sender')
    
    def with_receiver_info(self):
        """Optimize query by selecting related receiver information."""
        return self.select_related('receiver')
    
    def with_full_info(self):
        """Optimize query by selecting both sender and receiver information."""
        return self.select_related('sender', 'receiver')
    
    def only_essential_fields(self):
        """Use only() to limit fields for better performance."""
        return self.only('message_id', 'sender__email', 'content', 'timestamp', 'read')
    
    def unread_for_user_optimized(self, user):
        """Combined optimization for unread messages for a user."""
        return self.for_user(user).unread_only().with_sender_info().only_essential_fields()


# Custom Manager for Unread Messages
class UnreadMessagesManager(models.Manager):
    """
    Task 4: Custom manager that filters unread messages for a user.
    This manager provides optimized queries for unread message operations.
    """
    
    def get_queryset(self):
        """Return the custom QuerySet."""
        return MessageQuerySet(self.model, using=self._db)
    
    def for_user(self, user):
        """
        Get unread messages for a specific user.
        Uses optimization with select_related and only().
        """
        return self.get_queryset().unread_for_user_optimized(user)
    
    def unread_only(self):
        """Get all unread messages across all users."""
        return self.get_queryset().unread_only()
    
    def count_for_user(self, user):
        """Get count of unread messages for a user (optimized)."""
        return self.get_queryset().for_user(user).unread_only().count()
    
    def recent_unread_for_user(self, user, days=7):
        """Get recent unread messages for a user."""
        return self.get_queryset().for_user(user).unread_only().recent(days).with_sender_info()
    
    def mark_as_read_for_user(self, user, message_ids=None):
        """
        Mark messages as read for a user.
        If message_ids provided, mark only those messages.
        """
        queryset = self.get_queryset().for_user(user).unread_only()
        if message_ids:
            queryset = queryset.filter(message_id__in=message_ids)
        
        return queryset.update(read=True)


# Additional specialized managers
class MessageManager(models.Manager):
    """
    General message manager with common operations.
    """
    
    def get_queryset(self):
        return MessageQuerySet(self.model, using=self._db)
    
    def for_conversation(self, user1, user2):
        """Get messages between two users."""
        return self.get_queryset().filter(
            models.Q(sender=user1, receiver=user2) |
            models.Q(sender=user2, receiver=user1)
        ).with_full_info().order_by('timestamp')
    
    def unread_count_by_sender(self, user):
        """Get count of unread messages grouped by sender."""
        from django.db.models import Count
        return self.get_queryset().for_user(user).unread_only().values(
            'sender__email', 'sender__first_name', 'sender__last_name'
        ).annotate(unread_count=Count('message_id')).order_by('-unread_count')


class Message(models.Model):
    """
    Message model with read field and custom managers.
    """
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_sent')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_received')
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    edited = models.BooleanField(default=False)
    
    # Task 4: Add read boolean field to indicate whether a message has been read
    read = models.BooleanField(default=False)
    
    parent_message = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    def __str__(self):
        return f"Message from {self.sender.email} to {self.receiver.email} at {self.timestamp}"

    # Custom managers
    objects = MessageManager()  # Default manager
    unread_messages = UnreadMessagesManager()  # Task 4: Custom manager for unread messages

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['receiver', 'read']),  # Optimize unread message queries
            models.Index(fields=['sender', 'timestamp']),  # Optimize sent message queries
            models.Index(fields=['timestamp']),  # Optimize chronological queries
        ]


class Notification(models.Model):
    notification_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='notifications')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Notification for {self.user.email} about message {self.message.message_id}"


class MessageHistory(models.Model):
    history_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()
    edited_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"History for message {self.message.message_id} edited at {self.edited_at}"


# Usage examples for the custom managers:

"""
Example usage of the UnreadMessagesManager:

# Get all unread messages for a user
unread_messages = Message.unread_messages.for_user(user)

# Get count of unread messages
unread_count = Message.unread_messages.count_for_user(user)

# Get recent unread messages (last 7 days)
recent_unread = Message.unread_messages.recent_unread_for_user(user, days=7)

# Mark messages as read
Message.unread_messages.mark_as_read_for_user(user, message_ids=[msg1_id, msg2_id])

# Use in views with optimization
def unread_messages_view(request):
    unread_messages = Message.unread_messages.for_user(request.user)
    return render(request, 'unread_messages.html', {'messages': unread_messages})

# Get unread count by sender
unread_by_sender = Message.objects.unread_count_by_sender(user)
"""
