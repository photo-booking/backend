import base64

from django.core.files.base import ContentFile
from rest_framework import serializers
from djoser.serializers import (
    SendEmailResetSerializer,
    TokenCreateSerializer,
    UserCreateSerializer,

)

from orders.models import Chat, Message, Order, Raiting
from properties.models import FeedbackProperty, Property, Room
from services.models import MediaFile, Service, Tag
from users.models import User


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class TagsSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Tag."""

    class Meta:
        model = Tag
        fields = ('name', 'slug')


class ShortUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
        )


class ServiceSerializer(serializers.ModelSerializer):
    image_service = Base64ImageField(required=False, allow_null=True)
    tag = TagsSerializer(read_only=True, many=True)
    authors = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = (
            'authors',
            'name_service',
            'image_service',
            'cost_service',
            'description_service',
            'due_date',
            'equipment',
            'min_duration',
            'tag',
        )

    def get_authors(self, services, *args, **kwargs):
        authors = services.author.all()
        if authors is not None:
            return ShortUserSerializer(authors, many=True).data


class MediafileSerializer(serializers.ModelSerializer):
    authors = serializers.SerializerMethodField()

    class Meta:
        model = MediaFile
        fields = (
            'authors',
            'link',
            'title',
            'media_type',
            'is_main_photo',
        )

    def get_authors(self, media, *args, **kwargs):
        authors = media.author
        if authors is not None:
            return ShortUserSerializer(authors).data


class UserSerializer(serializers.ModelSerializer):
    profile_photo = Base64ImageField(required=False, allow_null=True)

    services = serializers.SerializerMethodField()
    mediafiles = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'profile_photo',
            'email',
            'contact_email',
            'phone',
            'work_experience',
            'city',
            'raiting',
            'about_me',
            'is_client',
            'is_photographer',
            'is_video_operator',
            'birthday',
            'social_telegram',
            'social_vkontakte',
            'services',
            'mediafiles',
        )

    def get_mediafiles(self, user, *args, **kwargs):
        foto = user.mediafiles.all()[:6]
        if foto is not None:
            return MediafileSerializer(foto, many=True).data

    def get_services(self, user, *args, **kwargs):
        services = user.services.all()
        if services is not None:
            return ServiceSerializer(services, many=True).data


class PropertySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Property
        fields = (
            'user',
            'name',
            'adress',
            'worktime',
            'area',
            'price',
        )


class RoomSerializer(serializers.ModelSerializer):
    property = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Room
        fields = (
            'property',
            'name',
            'area',
            'price',
        )


class FBpropertySerializer(serializers.ModelSerializer):
    property = serializers.StringRelatedField(read_only=True)
    user_client = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = FeedbackProperty
        fields = (
            'property',
            'raiting',
            'descriptions',
            'user_client',
        )


class GeneralCatalogExecutorCardSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    portfolio = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'full_name',
            'is_client',
            'is_photographer',
            'is_video_operator',
            'about_me',
            'price',
            'portfolio',
        )

    def get_full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'

    def get_price(self, obj):
        services = obj.services.all()
        if services:
            lower_price = services.order_by('cost_service')[0].cost_service
            return lower_price

    def get_portfolio(self, obj):
        all_media = obj.portfolio.all().order_by('media_file__media_type')
        selection = []
        if all_media:
            last_media = all_media[-1]
            if last_media.media_file.media_type == 'Video':
                selection.append(last_media.media_file.link)
            for i in range(4):
                media = all_media[i]
                selection.append(media.media_file.link)
                if len(selection) == 4:
                    break

        return selection


class ChatSerializer(serializers.ModelSerializer):
    users = serializers.StringRelatedField(read_only=True, many=True)

    class Meta:
        model = Chat
        fields = (
            'name',
            'users',
        )


class OrderSerializer(serializers.ModelSerializer):
    service = serializers.StringRelatedField(read_only=True)
    chat = serializers.StringRelatedField(read_only=True)
    users = serializers.StringRelatedField(read_only=True, many=True)

    class Meta:
        model = Order
        fields = (
            'name',
            'cost',
            'date',
            'completion_date',
            'status',
            'users',
            'service',
            'chat',
        )


class MessageSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Message
        fields = (
            'chat',
            'author',
            'text',
            'created_at',
        )


class RaitingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True, many=True)

    class Meta:
        model = Raiting
        fields = (
            'order',
            'user',
            'raiting',
        )


class CustomSendEmailResetSerializer(SendEmailResetSerializer):
    default_error_messages = {
        'email_not_found': 'Аккаунта с такой электронной почтой не существует'
    }


class CustomTokenCreateSerializer(TokenCreateSerializer):
    default_error_messages = {
        'invalid_credentials': 'Проверьте корректность ввода почты и пароля',
        'inactive_account': 'Этот аккаунт неактивен, \
        обратитесь в форму обратной связи',
    }


class CustomUserCreateSerializer(UserCreateSerializer):
    default_error_messages = {
        "cannot_create_user": 'Мы не можем создать пользователя, \
        обратитесь в форму обратной связи'
    }
