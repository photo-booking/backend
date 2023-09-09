from django.shortcuts import redirect, render
from django_filters.rest_framework import DjangoFilterBackend
from djoser.compat import get_user_email
from djoser.conf import settings
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

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


def user_token(request):
    if request.user.is_authenticated:
        token, e = Token.objects.get_or_create(user=request.user)
        return redirect(
            'https://photo-market.acceleratorpracticum.ru/sign-in/?token='
            + token.key
        )
    else:
        return redirect(
            'https://photo-market.acceleratorpracticum.ru/sign-in/?error=true'
        )


def index(request):
    context = {
        'users': User.objects.order_by('email')
        if request.user.is_authenticated
        else []
    }
    return render(request, 'index.html', context)


class UserViewSet(DjoserUserViewSet):
    #    queryset = User.objects.all()
    pagination_class = LimitPageNumberPagination
    search_fields = ['^first_name', '^last_name']
    filterset_class = UsersFilter
    filter_backends = [DjangoFilterBackend, SearchFilter]

    def get_queryset(self):
        queryset = User.objects.all()
        spec = self.request.query_params.get('spec')
        min_cost = self.request.query_params.get('min_cost')
        max_cost = self.request.query_params.get('max_cost')
        maxCost = self.request.query_params.get('maxCost')
        minCost = self.request.query_params.get('minCost')
        if spec is not None:
            if spec == 'photographer':
                queryset = queryset.filter(is_photographer=True)
            if spec == 'videographer':
                queryset = queryset.filter(is_video_operator=True)
            else:
                queryset = queryset.filter(
                    is_video_operator=True
                ) | queryset.filter(is_photographer=True)
        if min_cost is not None:
            queryset = queryset.order_by('services__cost_service')
        if max_cost is not None:
            queryset = queryset.order_by('-services__cost_service')
        if minCost is not None:
            queryset = queryset.filter(
                services__cost_service__range=(minCost, maxCost)
            )
        return queryset

    @action(['get', 'post'], detail=False)
    def reset_password(self, request, *args, **kwargs):
        if request.method == 'GET':
            return self.retrieve(request, *args, **kwargs)
        elif request.method == 'POST':
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.get_user()
            if user:
                context = {'user': user}
                to = [get_user_email(user)]
                settings.EMAIL.password_reset(self.request, context).send(to)

        return Response(status=status.HTTP_204_NO_CONTENT)


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
