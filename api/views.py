from djoser.views import UserViewSet as DjoserUserViewSet
from django.shortcuts import render
from rest_framework import viewsets

from api.paginators import LimitPageNumberPagination
from orders.models import Chat, Message, Order, Raiting
from properties.models import FeedbackProperty, Property, Room
from services.models import Service, MediaFile
from users.models import User

from .serializers import (
    ChatSerializer,
    FBpropertySerializer,
    MediafileSerializer,
    MessageSerializer,
    OrderSerializer,
    PropertySerializer,
    RaitingSerializer,
    RoomSerializer,
    ServiceSerializer,
)


def index(request):
    context = {
        'users': User.objects.order_by('email')
        if request.user.is_authenticated else []
    }
    return render(request, 'index.html', context)


class UserViewSet(DjoserUserViewSet):
    queryset = User.objects.all()
    pagination_class = LimitPageNumberPagination


class MediafileViewSet(viewsets.ModelViewSet):
    queryset = MediaFile.objects.all()
    serializer_class = MediafileSerializer


class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class FBpropertyViewSet(viewsets.ModelViewSet):
    queryset = FeedbackProperty.objects.all()
    serializer_class = FBpropertySerializer


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class RaitingViewSet(viewsets.ModelViewSet):
    queryset = Raiting.objects.all()
    serializer_class = RaitingSerializer
