import json

from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from djangochannelsrestframework import mixins
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.observer import model_observer
from djangochannelsrestframework.observer.generics import (
    ObserverModelInstanceMixin,
    action,
)
from rest_framework import permissions, status

from .models import Chat, Message
from .serializers import MessageSerializer, ShortUserSerializer

# from .serializers import RoomSerializer
User = get_user_model()


class ChatConsumer(ObserverModelInstanceMixin, GenericAsyncAPIConsumer):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    lookup_field = "pk"
    permission_classes = (permissions.AllowAny,)

    async def disconnect(self, code):
        if hasattr(self, "room_subscribe"):
            await self.remove_user_from_room(self.room_subscribe)
            await self.notify_users()
        await super().disconnect(code)

    @action()
    async def join_room(self, pk, **kwargs):
        self.room_subscribe = pk
        await self.add_user_to_room(pk)
        await self.notify_users()

    @action()
    async def leave_room(self, pk, **kwargs):
        await self.remove_user_from_room(pk)

    @action()
    async def create_message(self, message, **kwargs):
        room: Chat = await self.get_room(pk=self.room_subscribe)
        await database_sync_to_async(Message.objects.create)(
            chat=room.pk, user=self.scope["user"], text=message
        )

    @action()
    async def subscribe_to_messages_in_room(self, pk, **kwargs):
        await self.message_activity.subscribe(room=pk)

    @model_observer(Message)
    async def message_activity(self, message, observer=None, **kwargs):
        await self.send_json(message)

    @message_activity.groups_for_signal
    def message_activity(self, instance: Message, **kwargs):
        yield f'room__{instance.chat_id}'
        yield f'pk__{instance.pk}'

    @message_activity.groups_for_consumer
    def message_activity(self, room=None, **kwargs):
        if room is not None:
            yield f'room__{room}'

    @message_activity.serializer
    def message_activity(self, instance: Message, action, **kwargs):
        return dict(
            data=MessageSerializer(instance).data,
            action=action.value,
            pk=instance.pk,
        )

    async def notify_users(self):
        room: Chat = await self.get_room(self.room_subscribe)
        for group in self.groups:
            await self.channel_layer.group_send(
                group,
                {
                    'type': 'update_users',
                    'usuarios': await self.current_users(room),
                },
            )

    async def update_users(self, event: dict):
        await self.send(text_data=json.dumps({'usuarios': event["usuarios"]}))

    @database_sync_to_async
    def get_room(self, pk: int) -> Chat:
        return Chat.objects.get(pk=pk)

    @database_sync_to_async
    def current_users(self, room: Chat):
        return [
            ShortUserSerializer(user).data for user in room.current_users.all()
        ]

    @database_sync_to_async
    def remove_user_from_room(self, room):
        user: User = self.scope["user"]
        user.current_rooms.remove(room)

    @database_sync_to_async
    def add_user_to_room(self, pk):
        print(11111111111)
        print(self.scope["user"])
        user: User = self.scope["user"]
        if not user.current_rooms.filter(pk=self.room_subscribe).exists():
            user.current_rooms.add(Chat.objects.get(pk=pk))

    @action()
    @database_sync_to_async
    def create_massage(self, data: dict, **kwargs):
        print(1111111)
        print(data)
        serializer = MessageSerializer(data=data, action_kwargs=kwargs)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, **kwargs)
        return serializer.data, status.HTTP_201_CREATED


class UserConsumer(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.PatchModelMixin,
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin,
    mixins.DeleteModelMixin,
    GenericAsyncAPIConsumer,
):
    queryset = User.objects.all()
    serializer_class = ShortUserSerializer
