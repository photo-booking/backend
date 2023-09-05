from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from api.paginators import (
    CatalogPagination,
    LimitPageNumberPagination,
    PortfolioLimitPageNumberPagination,
)
from orders.models import Chat, Message, Order, Raiting
from properties.models import FeedbackProperty, Property, Room
from services.filters import CatalogFilter
from services.models import MediaFile, Service
from users.models import User

from .filters import UsersFilter
from .serializers import (
    ChatSerializer,
    FBpropertySerializer,
    GeneralCatalogExecutorCardSerializer,
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
    pagination_class = LimitPageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['^first_name', '^last_name']
    filterset_class = UsersFilter

    def get_queryset(self):
        queryset = User.objects.all()
        is_photographer = self.request.query_params.get('is_photographer')
        is_video_operator = self.request.query_params.get('is_video_operator')
        if is_photographer is not None:
            queryset = User.objects.filter(is_photographer=True)
            return queryset
        elif is_video_operator is not None:
            queryset = User.objects.filter(is_video_operator=True)
            return queryset
        return queryset


class MediafileViewSet(viewsets.ModelViewSet):
    queryset = MediaFile.objects.all()
    serializer_class = MediafileSerializer
    pagination_class = PortfolioLimitPageNumberPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


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


class GeneralCatalogExecutorCardViewSet(viewsets.ModelViewSet):
    queryset = User.objects.exclude(is_client=True)
    serializer_class = GeneralCatalogExecutorCardSerializer
    pagination_class = CatalogPagination
    filter_backends = [
        DjangoFilterBackend,
    ]
    filterset_class = CatalogFilter
    ordering_fields = ['services__cost_service']
    http_method_names = [
        'get',
    ]


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
