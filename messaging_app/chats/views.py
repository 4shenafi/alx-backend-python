# messaging_app/chats/views.py
from rest_framework import viewsets, filters  # Add filters import
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import User, Conversation, Message
from .serializers import UserSerializer, ConversationSerializer, MessageSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]  # Enable filtering and ordering
    search_fields = ['participants__email']  # Allow searching conversations by participant email
    ordering_fields = ['created_at']  # Allow ordering by creation time

    def perform_create(self, serializer):
        """Ensure the authenticated user is added as a participant."""
        conversation = serializer.save()
        conversation.participants.add(self.request.user)
        return conversation

    @action(detail=True, methods=['post'])
    def add_message(self, request, pk=None):
        """Custom action to add a message to a conversation."""
        conversation = self.get_object()
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(conversation=conversation, sender=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]  # Enable filtering and ordering
    search_fields = ['message_body']  # Allow searching messages by content
    ordering_fields = ['sent_at']  # Allow ordering by sent time

    def get_queryset(self):
        """Optionally filter messages by conversation ID."""
        queryset = super().get_queryset()
        conversation_id = self.request.query_params.get('conversation_id')
        if conversation_id:
            queryset = queryset.filter(conversation__conversation_id=conversation_id)
        return queryset