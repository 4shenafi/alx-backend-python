from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Message, Notification, MessageHistory


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('message_id', 'sender', 'receiver', 'timestamp', 'edited', 'read')
    list_filter = ('edited', 'read', 'timestamp')
    search_fields = ('sender__email', 'receiver__email', 'content')
    readonly_fields = ('message_id', 'timestamp')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('sender', 'receiver', 'parent_message')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('notification_id', 'user', 'message', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__email', 'message__content')
    readonly_fields = ('notification_id', 'created_at')


@admin.register(MessageHistory)
class MessageHistoryAdmin(admin.ModelAdmin):
    list_display = ('history_id', 'message', 'edited_at')
    list_filter = ('edited_at',)
    search_fields = ('message__content', 'old_content')
    readonly_fields = ('history_id', 'edited_at')
