from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Custom permission: only allow users to access their own objects.
    """

    def has_object_permission(self, request, view, obj):
        # Assuming your model has a user field
        return hasattr(obj, "user") and obj.user == request.user


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission:
    - Only allow authenticated users
    - Only participants of a conversation can send, view, update, or delete messages
    """

    def has_permission(self, request, view):
        # User must be authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user

        # Case 1: object is a Conversation
        if hasattr(obj, "participants"):
            if user not in obj.participants.all():
                return False

        # Case 2: object is a Message
        if hasattr(obj, "conversation"):
            if user not in obj.conversation.participants.all():
                return False

        # Explicitly check methods: only participants can update or delete
        if request.method in ["PUT", "PATCH", "DELETE"]:
            return True  # already confirmed user is a participant

        # GET, POST allowed if participant
        if request.method in ["GET", "POST"]:
            return True

        return False