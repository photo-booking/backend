from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from api.paginators import (
    LimitPageNumberPagination,
    PortfolioLimitPageNumberPagination,
)
from orders.models import Chat, Message, Order, Raiting
from properties.models import Feedback_property, Property, Room
from services.models import Service
from users.models import Media_file, User

from .filters import UsersFilter
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
        if request.user.is_authenticated
        else []
    }
    return render(request, 'index.html', context)


class UserViewSet(DjoserUserViewSet):
    queryset = User.objects.all()
    pagination_class = LimitPageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['^first_name', '^last_name']
    filterset_class = UsersFilter

    def perform_create(self, serializer):
        print(self.request.user)
        serializer.save(user=self.request.user)

    # def get_queryset(self):
    #     queryset = User.objects.all()
    #     is_photographer = self.request.query_params.get('is_photographer')
    # is_video_operator = self.request.query_params.get('is_video_operator')
    #     if is_photographer is not None:
    #         queryset = User.objects.filter(is_photographer=True)
    #         return queryset
    #     elif is_video_operator is not None:
    #         queryset = User.objects.filter(is_video_operator=True)
    #         return queryset
    #     return queryset


class MediafileViewSet(viewsets.ModelViewSet):
    queryset = Media_file.objects.all()
    serializer_class = MediafileSerializer
    pagination_class = PortfolioLimitPageNumberPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class FBpropertyViewSet(viewsets.ModelViewSet):
    queryset = Feedback_property.objects.all()
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
