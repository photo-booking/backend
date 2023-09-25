from django.urls import path

from .views import order_chat_room

app_name = 'chat'


urlpatterns = [
    path('room/<int:order_id>/', order_chat_room, name='order_chat_room'),
]
