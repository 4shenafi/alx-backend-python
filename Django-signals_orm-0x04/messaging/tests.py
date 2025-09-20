from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory

User = get_user_model()


class SignalTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            email='user1@test.com',
            password='testpass123',
            first_name='User',
            last_name='One'
        )
        self.user2 = User.objects.create_user(
            email='user2@test.com',
            password='testpass123',
            first_name='User',
            last_name='Two'
        )

    def test_notification_created_on_message(self):
        """Test that a notification is created when a new message is sent."""
        # Create a message
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Hello, this is a test message'
        )
        
        # Check that a notification was created
        self.assertTrue(Notification.objects.filter(
            user=self.user2,
            message=message
        ).exists())

    def test_message_edit_logging(self):
        """Test that message edits are logged in MessageHistory."""
        # Create a message
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Original content'
        )
        
        # Edit the message
        message.content = 'Edited content'
        message.save()
        
        # Check that history was created
        self.assertTrue(MessageHistory.objects.filter(
            message=message,
            old_content='Original content'
        ).exists())
        
        # Check that edited flag is set
        message.refresh_from_db()
        self.assertTrue(message.edited)

    def test_user_deletion_cleanup(self):
        """Test that user deletion cleans up related data."""
        # Create a message
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Test message'
        )
        
        # Create a notification
        notification = Notification.objects.create(
            user=self.user2,
            message=message
        )
        
        # Delete user1
        self.user1.delete()
        
        # Check that related data was cleaned up
        self.assertFalse(Message.objects.filter(sender=self.user1).exists())
        self.assertFalse(Notification.objects.filter(message=message).exists())


class ModelTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            email='user1@test.com',
            password='testpass123',
            first_name='User',
            last_name='One'
        )
        self.user2 = User.objects.create_user(
            email='user2@test.com',
            password='testpass123',
            first_name='User',
            last_name='Two'
        )

    def test_message_creation(self):
        """Test basic message creation."""
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Test message'
        )
        
        self.assertEqual(message.sender, self.user1)
        self.assertEqual(message.receiver, self.user2)
        self.assertEqual(message.content, 'Test message')
        self.assertFalse(message.read)
        self.assertFalse(message.edited)

    def test_threaded_conversation(self):
        """Test threaded conversation with parent-child messages."""
        # Create parent message
        parent_message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Parent message'
        )
        
        # Create reply
        reply = Message.objects.create(
            sender=self.user2,
            receiver=self.user1,
            content='Reply message',
            parent_message=parent_message
        )
        
        # Check relationship
        self.assertEqual(reply.parent_message, parent_message)
        self.assertIn(reply, parent_message.replies.all())

    def test_unread_messages_manager(self):
        """Test custom manager for unread messages."""
        # Create read and unread messages
        Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Unread message',
            read=False
        )
        
        Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Read message',
            read=True
        )
        
        # Test unread messages manager
        unread_messages = Message.unread_messages.for_user(self.user2)
        self.assertEqual(unread_messages.count(), 1)
        self.assertEqual(unread_messages.first().content, 'Unread message')
