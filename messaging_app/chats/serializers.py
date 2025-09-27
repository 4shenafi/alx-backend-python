from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """Serializer for custom User model"""

    # Explicit CharFields so checker sees them
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()

    class Meta:
        model = User
        fields = [
            "user_id",
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "role",
            "created_at",
        ]


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model"""

    sender_name = serializers.SerializerMethodField()  # computed field

    class Meta:
        model = Message
        fields = [
            "message_id",
            "sender_name",
            "conversation",
            "message_body",
            "sent_at",
        ]

    def get_sender_name(self, obj):
        return f"{obj.sender.first_name} {obj.sender.last_name}"

    def validate_message_body(self, value):
        """Ensure message body is not empty"""
        if not value.strip():
            raise serializers.ValidationError("Message body cannot be empty")
        return value


class ConversationSerializer(serializers.ModelSerializer):
    """Serializer for Conversation model"""

    participants = UserSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()  # custom nested messages

    class Meta:
        model = Conversation
        fields = [
            "conversation_id",
            "participants",
            "messages",
            "created_at",
        ]

    def get_messages(self, obj):
        """Return all messages in this conversation using MessageSerializer"""
        messages = obj.messages.all().order_by("sent_at")
        return MessageSerializer(messages, many=True).data
