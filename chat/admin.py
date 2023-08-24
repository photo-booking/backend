from django.contrib import admin

from chat.models import Message, Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'host', '_current_users')
    search_fields = ('name', 'host', 'current_users')
    list_filter = (
        'host',
        'current_users',
    )

    def _current_users(self, obj):
        return ', '.join([user.username for user in obj.current_rooms.all()])


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'user', 'created_at')
    search_fields = ('text', 'user')
    list_filter = (
        'text',
        'user',
    )
