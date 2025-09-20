from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    """
    def has_object_permission(self, request, view, obj):
        # Check if the user is a participant of the conversation.
        # obj.participants is a ManyToMany field, so we use .all() to get the list of users.
        return request.user in obj.participants.all()