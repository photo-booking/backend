import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone
from djangochannelsrestframework.observer.generics import action

from chat.models import Chat, Message
from photo_booking import settings

timezone.activate(settings.TIME_ZONE)


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.id = self.scope['url_route']['kwargs']['chat_id']
        self.room_group_name = f'chat_{self.id}'
        self.user = self.scope['user']
        # присоединиться к группе чат-комнаты
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        # принять соединение
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    @database_sync_to_async
    def get_chat(self, pk: int) -> Chat:
        return Chat.objects.get(pk=pk)

    @database_sync_to_async
    def get_message(self) -> Message:
        return Message.objects.latest('created_at')

    # получить сообщение из WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        text = text_data_json['message']
        types = text_data_json['type']
        now = timezone.now()
        chat: Chat = await self.get_chat(pk=self.id)
        if types == "received":
            pk = text_data_json['pk']
            message: Message = await self.get_name(pk)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'pk': message.pk,
                    'chat': chat.pk,
                    'type': types,
                    'text': message.text,
                    'user': self.user.first_name,
                    'received': message.received,
                },
            )
            self.send(
                text_data=json.dumps(
                    {'message': message.text, 'received': 'True'}
                )
            )
        else:
            await database_sync_to_async(Message.objects.create)(
                chat=chat, user=self.scope["user"], text=text
            )
            message: Message = await self.get_message()
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'pk': message.pk,
                    'chat': chat.pk,
                    'type': types,
                    'text': text,
                    'user': self.user.first_name,
                    'received': message.received,
                    'created_at': now.astimezone().isoformat(
                        timespec='minutes', sep=" "
                    ),
                },
            )

            # отправить сообщение в WebSocket
            self.send(text_data=json.dumps({'message': text}))

    @action
    async def receive_messages(self, pk, **kwargs):
        chat: Chat = await self.get_chat(pk=self.id)
        self.send(text_data=json.dumps({'message': chat.messages.all()}))

    # получить сообщение из группы чат-комнаты
    async def chat_message(self, event):
        # отправить сообщение в веб-сокет
        await self.send(text_data=json.dumps(event))

    # проверить статус сообщения из группы чат-комнаты
    async def received(self, event):
        # отправить сообщение в веб-сокет
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def get_name(self, pk):
        message = Message.objects.get(pk=pk)
        message.received = True
        message.save()
        return message
