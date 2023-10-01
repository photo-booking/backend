from rest_framework import serializers

from api.serializers import ShortUserSerializer

from .models import Chat, Message


class MessageSerializer(serializers.ModelSerializer):
    created_at_formatted = serializers.SerializerMethodField()
    user = ShortUserSerializer()

    class Meta:
        model = Message
        exclude = []
        depth = 1

    def get_created_at_formatted(self, obj: Message):
        return obj.created_at.strftime("%d-%m-%Y %H:%M:%S")


class RoomSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Chat
        fields = [
            "pk",
            "name",
            "host",
            "messages",
            "current_users",
            "last_message",
        ]
        depth = 1
        read_only_fields = ["messages", "last_message"]

    def get_last_message(self, obj: Chat):
        return MessageSerializer(
            obj.messages.order_by('created_at').last()
        ).data
