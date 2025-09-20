# Django Signals, ORM, and Caching Project

This project demonstrates advanced Django concepts including Django Signals, ORM optimization techniques, and basic caching strategies.

## Features Implemented

### 1. Django Signals (Tasks 0-2)

#### Task 0: User Notifications
- **File**: `messaging/models.py`, `messaging/signals.py`, `messaging/apps.py`, `messaging/admin.py`, `messaging/tests.py`
- **Implementation**: 
  - `Message` model with sender, receiver, content, and timestamp fields
  - `Notification` model linked to User and Message models
  - `post_save` signal that automatically creates notifications when new messages are sent
  - Signal registration in `apps.py` to ensure signals are loaded

#### Task 1: Message Edit Logging
- **File**: `messaging/models.py`, `messaging/signals.py`
- **Implementation**:
  - Added `edited` field to Message model
  - `MessageHistory` model to store old content before edits
  - `pre_save` signal that logs old content before message updates
  - Automatic setting of `edited` flag when content changes

#### Task 2: User Deletion Cleanup
- **File**: `messaging/Views/views.py`, `messaging/signals.py`
- **Implementation**:
  - `delete_user` view for account deletion
  - `post_delete` signal on User model that automatically cleans up:
    - All messages sent by the user
    - All messages received by the user
    - All notifications for the user
    - All message history for user's messages
  - Respects foreign key constraints with CASCADE deletion

### 2. Advanced ORM Techniques (Tasks 3-4)

#### Task 3: Threaded Conversations
- **File**: `Django-Chat/Models`
- **Implementation**:
  - `ThreadedMessage` model with self-referential `parent_message` field
  - Advanced ORM queries using `select_related` and `prefetch_related`
  - Recursive query methods for fetching message threads
  - Custom QuerySet and Manager for optimized operations
  - Thread depth calculation for proper display

#### Task 4: Custom ORM Manager for Unread Messages
- **File**: `messaging/Models/models.py`
- **Implementation**:
  - Added `read` boolean field to Message model
  - `UnreadMessagesManager` custom manager with methods:
    - `for_user()` - Get unread messages for specific user
    - `unread_only()` - Filter only unread messages
    - `count_for_user()` - Get unread count
    - `mark_as_read_for_user()` - Mark messages as read
  - Optimized queries using `select_related` and `only()`
  - Database indexes for performance optimization

### 3. Basic Caching (Task 5)

#### Task 5: View-Level Caching
- **File**: `messaging_app/messaging_app/settings.py`, `chats/views.py`
- **Implementation**:
  - Configured `LocMemCache` in settings.py
  - Added `@cache_page(60)` decorator to MessageViewSet list view
  - 60-second cache timeout for message list views
  - Cache configuration using `django.core.cache.backends.locmem.LocMemCache`

## Project Structure

```
Django-signals_orm-0x04/
├── manage.py
├── requirements.txt
├── README.md
├── messaging_app/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── messaging/
│   ├── __init__.py
│   ├── models.py
│   ├── signals.py
│   ├── apps.py
│   ├── admin.py
│   ├── views.py
│   ├── urls.py
│   ├── tests.py
│   ├── Models/
│   │   └── models.py
│   └── Views/
│       └── views.py
└── Django-Chat/
    └── Models
```

## Key Django Concepts Demonstrated

### Django Signals
- **post_save**: Automatic notification creation
- **pre_save**: Message edit logging
- **post_delete**: User data cleanup
- Signal registration and best practices

### Advanced ORM Techniques
- **select_related**: Foreign key optimization (JOINs)
- **prefetch_related**: Many-to-many and reverse foreign key optimization
- **Custom Managers**: Encapsulated query logic
- **Custom QuerySets**: Reusable filtering methods
- **Database Indexes**: Performance optimization
- **only()**: Field limiting for better performance

### Caching Strategies
- **View-level caching**: Using `@cache_page` decorator
- **Cache configuration**: LocMemCache setup
- **Cache timeout**: 60-second expiration

## Usage Examples

### Using Custom Manager for Unread Messages
```python
# Get unread messages for a user
unread_messages = Message.unread_messages.for_user(user)

# Get count of unread messages
unread_count = Message.unread_messages.count_for_user(user)

# Mark messages as read
Message.unread_messages.mark_as_read_for_user(user, message_ids=[msg1_id, msg2_id])
```

### Threaded Conversations
```python
# Get threaded conversation between two users
messages = ThreadedMessage.get_threaded_conversation(user1, user2)

# Get message thread with replies
thread = ThreadedMessage.get_message_thread(message_id)
```

### Signal Usage
```python
# Signals are automatically triggered:
# - When a message is created (creates notification)
# - When a message is edited (logs history)
# - When a user is deleted (cleans up data)
```

## Testing

Run the test suite to verify signal functionality:
```bash
python manage.py test messaging
```

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

3. Create superuser:
```bash
python manage.py createsuperuser
```

4. Run development server:
```bash
python manage.py runserver
```

## Performance Optimizations

- Database indexes on frequently queried fields
- `select_related` for foreign key relationships
- `prefetch_related` for many-to-many relationships
- `only()` for limiting field retrieval
- View-level caching for expensive operations
- Custom managers for optimized queries

This project demonstrates production-ready Django patterns for building scalable, maintainable backend systems with proper separation of concerns and performance optimization.
