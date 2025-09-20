# Task 2: Views for User Deletion with Signal-based Cleanup
# This file contains views that demonstrate user deletion with automatic cleanup

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction

User = get_user_model()


@login_required
@require_http_methods(["DELETE"])
def delete_user_view(request):
    """
    Task 2: Delete user account view that triggers post_delete signal.
    The signal will automatically clean up all related data including:
    - Messages sent by the user
    - Messages received by the user  
    - Notifications for the user
    - Message history for user's messages
    """
    try:
        user = request.user
        
        # The post_delete signal in signals.py will handle cleanup automatically
        # This includes CASCADE deletion respecting foreign key constraints
        user.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'User account and all related data deleted successfully'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Failed to delete user account: {str(e)}'
        }, status=500)


class DeleteUserView(LoginRequiredMixin, DeleteView):
    """
    Class-based view for user account deletion with confirmation.
    """
    model = User
    template_name = 'messaging/delete_user_confirm.html'
    success_url = reverse_lazy('login')
    
    def get_object(self):
        return self.request.user
    
    def delete(self, request, *args, **kwargs):
        """
        Override delete method to ensure proper cleanup.
        The post_delete signal will handle all related data cleanup.
        """
        try:
            with transaction.atomic():
                # Get user before deletion for logging
                user = self.get_object()
                user_email = user.email
                
                # Delete user - this triggers the post_delete signal
                response = super().delete(request, *args, **kwargs)
                
                # Add success message
                messages.success(
                    request, 
                    f'Account {user_email} and all related data have been deleted successfully.'
                )
                
                return response
                
        except Exception as e:
            messages.error(
                request, 
                f'Failed to delete account: {str(e)}'
            )
            return self.get(request, *args, **kwargs)


@login_required
def user_deletion_confirmation(request):
    """
    View to show user deletion confirmation page with information about
    what data will be deleted (handled by signals).
    """
    user = request.user
    
    # Get counts of data that will be deleted
    from messaging.models import Message, Notification, MessageHistory
    
    messages_sent_count = Message.objects.filter(sender=user).count()
    messages_received_count = Message.objects.filter(receiver=user).count()
    notifications_count = Notification.objects.filter(user=user).count()
    
    context = {
        'user': user,
        'messages_sent_count': messages_sent_count,
        'messages_received_count': messages_received_count,
        'notifications_count': notifications_count,
        'total_messages': messages_sent_count + messages_received_count,
    }
    
    return render(request, 'messaging/delete_user_confirm.html', context)


@login_required
@require_http_methods(["POST"])
def confirm_user_deletion(request):
    """
    Confirmation endpoint for user deletion.
    """
    if request.POST.get('confirm') == 'yes':
        return delete_user_view(request)
    else:
        return JsonResponse({
            'success': False,
            'message': 'User deletion cancelled'
        })


# Additional views for demonstrating signal-based cleanup

@login_required
def user_data_summary(request):
    """
    View to show summary of user data that would be affected by deletion.
    This demonstrates what the post_delete signal will clean up.
    """
    user = request.user
    
    from messaging.models import Message, Notification, MessageHistory
    
    # Get user's data
    sent_messages = Message.objects.filter(sender=user).select_related('receiver')
    received_messages = Message.objects.filter(receiver=user).select_related('sender')
    notifications = Notification.objects.filter(user=user).select_related('message')
    
    # Get message history for user's messages
    user_message_ids = list(sent_messages.values_list('message_id', flat=True)) + \
                      list(received_messages.values_list('message_id', flat=True))
    message_history = MessageHistory.objects.filter(message_id__in=user_message_ids)
    
    context = {
        'user': user,
        'sent_messages': sent_messages[:10],  # Show first 10
        'received_messages': received_messages[:10],
        'notifications': notifications[:10],
        'message_history': message_history[:10],
        'total_sent': sent_messages.count(),
        'total_received': received_messages.count(),
        'total_notifications': notifications.count(),
        'total_history': message_history.count(),
    }
    
    return render(request, 'messaging/user_data_summary.html', context)
