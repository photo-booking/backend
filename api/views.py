import logging
from datetime import datetime, timedelta, timezone

import jwt
import requests
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from djoser.compat import get_user_email
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import serializers, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.action_social import create_google_user, create_vk_user
from api.paginators import (
    CatalogPagination,
    LimitPageNumberPagination,
    PortfolioLimitPageNumberPagination,
)
from chat.models import Chat, Message
from data import tags
from orders.models import Order, Raiting
from properties.models import FeedbackProperty, Property, Room
from services.models import MediaFile, Service, Tag
from users.models import User

from .filters import UsersFilter
from .serializers import (
    ChatSerializer,
    CountUserSerializer,
    FBpropertySerializer,
    GeneralCatalogExecutorCardSerializer,
    MediafileSerializer,
    MessageSerializer,
    OrderSerializer,
    PropertySerializer,
    RaitingSerializer,
    RoomSerializer,
    ServiceSerializer,
    SocialUserSerializer,
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)


class UserViewSet(DjoserUserViewSet):
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

    @action(['POST', 'GET'], detail=False)
    def reset_password(self, request, *args, **kwargs):
        if request.method == 'GET':
            return self.list(request, *args, **kwargs)
        elif request.method == 'POST':
            serializer = self.get_serializer(data=request.data)
            logging.info(f'value serializer {serializer}')
            serializer.is_valid(raise_exception=True)
            try:
                user = serializer.get_user()
                logging.info(f'user serializer {user}')
                if user:
                    context = {"user": user}
                    logging.info(f'context {context}')
                    to = get_user_email(user)
                    url_reset = 'https://photomarket.sytes.net/reset-password'
                    secret = 'jwt_secret'
                    payload_email = {
                        'exp': datetime.now(timezone.utc) + timedelta(hours=1),
                        'token': user.email,
                    }
                    logging.info(f'payload: {payload_email}')
                    payload_id = {
                        'exp': datetime.now(timezone.utc) + timedelta(hours=1),
                        'token': user.id,
                    }
                    logging.info(f'payload: {payload_id}')
                    token = jwt.encode(
                        payload_email, secret, algorithm='HS256'
                    )
                    logging.info(f'token {token}')
                    token_id = jwt.encode(
                        payload_id, secret, algorithm='HS256'
                    )
                    claims = jwt.decode(token, secret, algorithms=['HS256'])
                    logging.info(f'decode: {claims}')
                    claims_id = jwt.decode(
                        token_id, secret, algorithms=['HS256']
                    )
                    logging.info(f'decode id: {claims_id}')
                    url = (
                        'https://portfolio-polyntseva.'
                        'duckdns.org/sendemail/send_email'
                    )
                    data = {
                        'user': f'{settings.EMAIL_HOST_USER}',
                        'pass': f'{settings.EMAIL_HOST_PASSWORD}',
                        'from': f'{settings.EMAIL_HOST_USER}',
                        'to': f'{to}',
                        'subject': 'Сброс пароля',
                        'text': f'{url_reset}?uid={token_id}&token={token}',
                    }
                    requests.post(url, json=data)
                    return Response(status=status.HTTP_200_OK)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                logging.critical('Error:', exc_info=e)
                return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(['POST'], detail=False)
    def reset_password_confirm(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        logging.info(f'value serializer {serializer}')
        serializer.is_valid(raise_exception=True)
        logging.info(f'valid {serializer.is_valid(raise_exception=True)}')
        datas = serializer.data
        logging.info(f'serializer data: {datas}')
        current_time = int(round(datetime.now(timezone.utc).timestamp()))
        logging.info(f'current time: {current_time}')
        secret = 'jwt_secret'
        token_time = jwt.decode(datas.get('uid'), secret, algorithms=['HS256'])
        logging.info(f'token_time: {token_time}')
        if current_time > token_time['exp']:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            decode_token = jwt.decode(
                datas.get('token'), secret, algorithms=['HS256']
            )
            logging.info(f'decode_token: {decode_token}')
            email = decode_token['token']
            logging.info(f'email: {email}')
            try:
                user = User.objects.get(email=email)
                new_password = datas.get('new_password')
                logging.info(f'user: {user}')
                user.set_password(new_password)
                logging.info(f'password: {new_password}')
                user.save()
                return Response(
                    {'message': 'Password changed successfully.'},
                    status=status.HTTP_200_OK,
                )
            except Exception as e:
                logging.critical('Error:', exc_info=e)
                return Response(status=status.HTTP_400_BAD_REQUEST)


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

    def create(self, request, *args, **kwargs):
        data = request.data
        try:
            name_service = data['name_service']
            cost_service = data['cost_service']
            description_service = data['description_service']
            order_delivery_time = data['order_delivery_time']
            #            image_service=data['image_service']
            min_duration = data['min_duration']
        except KeyError as error:
            raise serializers.ValidationError(f"Отсутствует поле {error}")
        new_service = Service.objects.create(
            author=request.user,
            name_service=name_service,
            #                image_service=image_service,
            cost_service=cost_service,
            description_service=description_service,
            order_delivery_time=order_delivery_time,
            min_duration=min_duration,
        )
        new_service.save()
        try:
            for tag_s in data['tag']:
                try:
                    tag_obj = Tag.objects.get(name=tag_s['name'])
                except Tag.DoesNotExist:
                    raise serializers.ValidationError(
                        f"Выберети таг из списка {tags.tags}"
                    )
                new_service.tag.add(tag_obj)
        except KeyError as error:
            raise serializers.ValidationError(f"Отсутствует поле {error}")
        serialazer = ServiceSerializer(new_service)
        return Response(status=status.HTTP_201_CREATED, data=serialazer.data)


class GeneralCatalogExecutorCardViewSet(viewsets.ModelViewSet):
    serializer_class = GeneralCatalogExecutorCardSerializer
    pagination_class = CatalogPagination

    def get_queryset(self):
        type_of_shooting = {
            'aerial': 'aerial',
            'clips': 'clips',
            'family': 'family',
            'fashion': 'fashion',
            'individual': 'individual',
            'interview': 'interview',
            'lovestory': 'lovestory',
            'pets': 'pets',
            'stock': 'stock',
            'wedding': 'wedding',
        }

        serializer = self.get_serializer(data=self.request.data)
        queryset = User.objects.exclude(is_client=True)

        for param, value in serializer.initial_data.items():
            if param == 'expert':
                if value == 'photographer':
                    queryset = queryset.filter(is_photographer=True)
                elif value == 'video_operator':
                    queryset = queryset.filter(is_video_operator=True)

            if param == 'maxCost':
                queryset = queryset.filter(services__cost_service__lte=value)

            if param == 'minCost':
                queryset = queryset.filter(services__cost_service__gte=value)

            if param == 'isMaxCost' and value == 'True':
                queryset = queryset.order_by('-services__cost_service')

            if param == 'isMinCost' and value == 'True':
                queryset = queryset.order_by('services__cost_service')

            if param == 'typeOfShooting' and value:
                for type_, bool_ in value.items():
                    if type_ in type_of_shooting and bool_ == 'True':
                        queryset = queryset.filter(
                            services__name_service=type_
                        )

        return queryset


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    @action(
        methods=[
            'post',
        ],
        detail=False,
    )
    def check_chat(self, request, id=2):
        print(request.META['HTTP_ID'])
        id = request.META['HTTP_ID']
        user = request.user
        if request.method == 'POST':
            current_users = User.objects.get(pk=id)
            if Chat.objects.filter(
                host=user.pk, current_users=current_users
            ).exists():
                room = Chat.objects.get(
                    host=user.pk, current_users=current_users
                )
                serializer = ChatSerializer(room)
                return Response(serializer.data, status=status.HTTP_200_OK)
            elif Chat.objects.filter(
                host=current_users, current_users=user.pk
            ).exists():
                room = Chat.objects.get(
                    host=current_users, current_users=user.pk
                )
                serializer = ChatSerializer(room)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                room = Chat.objects.create(
                    host=user, name=(current_users.pk, user.pk)
                )
                room.current_users.add(current_users)

                serializer = ChatSerializer(room)
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class RaitingViewSet(viewsets.ModelViewSet):
    queryset = Raiting.objects.all()
    serializer_class = RaitingSerializer


@api_view(['GET'])
def count_user(request):
    return Response(CountUserSerializer(request).data)


def user_token(user):
    token, _ = Token.objects.get_or_create(user=user)
    logging.info(f'user token: {token.key}')
    return token.key


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token_user_from_google(request):
    serializer = SocialUserSerializer(data=request.data)
    logging.info(f'serialier data: {serializer.initial_data}')
    serializer.is_valid(raise_exception=True)
    token = serializer.initial_data.get('eccses_token')
    try:
        user = create_google_user(token)
        logging.info(f'user created - {user}')
    except Exception as e:
        logging.critical('Error:', exc_info=e)
        return Response(status=status.HTTP_502_BAD_GATEWAY)
    else:
        token_bd = user_token(user[0])
        return Response(
            status=status.HTTP_200_OK, data={'auth_token': {token_bd}}
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token_from_vk_user(request):
    serializer = SocialUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    code = serializer.initial_data.get('code')
    try:
        user = create_vk_user(code)
        logging.info(f'New user: {user[0]}')
    except Exception as e:
        logging.critical('Error:', exc_info=e)
        return Response(status=status.HTTP_502_BAD_GATEWAY)
    else:
        token_bd = user_token(user[0])
        return Response(
            status=status.HTTP_200_OK, data={'auth_token': {token_bd}}
        )
