from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model
from django.db.models import Prefetch, Q
from .models import Message, Notification, MessageHistory

User = get_user_model()


@cache_page(60)  # Cache for 60 seconds
def conversation_messages(request, user_id):
    """
    Task 5: Cached view to display messages in a conversation.
    Uses advanced ORM techniques with prefetch_related for optimization.
    """
    other_user = get_object_or_404(User, user_id=user_id)
    
    # Get messages between current user and other user
    messages = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user)
    ).select_related('sender', 'receiver', 'parent_message').prefetch_related(
        'replies__sender',
        'replies__receiver',
        'history'
    ).order_by('timestamp')
    
    # Get threaded messages (messages with replies)
    threaded_messages = []
    for message in messages:
        if not message.parent_message:  # Top-level message
            threaded_messages.append({
                'message': message,
                'replies': message.replies.all().order_by('timestamp')
            })
    
    return render(request, 'messaging/conversation.html', {
        'messages': threaded_messages,
        'other_user': other_user
    })


@login_required
@require_http_methods(["DELETE"])
def delete_user(request):
    """
    Task 2: Delete user account and clean up related data.
    The post_delete signal will handle the cleanup automatically.
    """
    try:
        user = request.user
        user.delete()  # This will trigger the post_delete signal
        return JsonResponse({'message': 'User account deleted successfully'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def unread_messages(request):
    """
    Task 4: Display unread messages using custom manager.
    """
    unread_messages = Message.unread_messages.for_user(request.user).only(
        'message_id', 'sender__email', 'content', 'timestamp'
    )
    
    return render(request, 'messaging/unread_messages.html', {
        'unread_messages': unread_messages
    })


@login_required
def message_history(request, message_id):
    """
    Task 1: Display message edit history.
    """
    message = get_object_or_404(Message, message_id=message_id)
    history = MessageHistory.objects.filter(message=message).order_by('-edited_at')
    
    return render(request, 'messaging/message_history.html', {
        'message': message,
        'history': history
    })
