from django.shortcuts import get_object_or_404, render
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import viewsets

from api.paginators import (
    CatalogPagination,
    LimitPageNumberPagination,
    ServicePagination,
)
from orders.models import Chat, Message, Order, Raiting
from properties.models import FeedbackProperty, Property, Room
from services.filters import CatalogFilter, ServiceFilter
from services.models import MediaFile, Service
from users.models import User

from .serializers import (
    CatalogDetailSerializer,
    ChatSerializer,
    FBpropertySerializer,
    GeneralCatalogExecutorCardSerializer,
    MediafileSerializer,
    MessageSerializer,
    OrderSerializer,
    PropertySerializer,
    RaitingSerializer,
    RoomSerializer,
    ServiceLimitedMediaSerializer,
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

    def get_serializer_class(self):
        if self.action == 'list':
            return GeneralCatalogExecutorCardSerializer
        return CatalogDetailSerializer


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


class ExecutorServiceViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceLimitedMediaSerializer
    pagination_class = ServicePagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ServiceFilter
    ordering_fields = ('cost_service',)

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        worker = get_object_or_404(User, pk=user_id)
        self.expert = CatalogDetailSerializer(worker).data
        return worker.services.all()

    def get_paginated_response(self, data):
        return self.paginator.get_paginated_response(data, self.expert)

    def get_serializer_class(self):
        if self.action == 'list':
            return ServiceLimitedMediaSerializer
        return ServiceSerializer
