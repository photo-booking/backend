from django.contrib import admin

from chat.models import Chat, Message


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'host', '_current_users')
    search_fields = ('name', 'host', 'current_users')
    list_filter = (
        'host',
        'current_users',
    )

    def _current_users(self, obj):
        return ', '.join([user.first_name for user in obj.current_users.all()])


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'user', 'created_at')
    search_fields = ('text', 'user')
    list_filter = (
        'text',
        'user',
    )
