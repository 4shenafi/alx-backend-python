from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    class Meta:
        model = User
        fields = [
            'user_id', 'first_name', 'last_name', 'full_name',
            'email', 'phone_number', 'role', 'created_at'
        ]


class MessageSerializer(serializers.ModelSerializer):
    sender_email = serializers.SerializerMethodField()
    message_body = serializers.CharField(max_length=2000)

    def get_sender_email(self, obj):
        return obj.sender.email

    class Meta:
        model = Message
        fields = [
            'message_id', 'sender_email', 'conversation',
            'message_body', 'sent_at', 'is_read'
        ]


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    def validate(self, data):
        # Example validation: don't allow empty conversations (this is just illustrative)
        if not data.get("participants") and self.instance is None:
            raise serializers.ValidationError("A conversation must include at least one participant.")
        return data

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages']
