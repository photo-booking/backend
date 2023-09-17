import base64

from django.core.files.base import ContentFile
from djoser.serializers import (
    SendEmailResetSerializer,
    TokenCreateSerializer,
    UserCreateSerializer,
)
from rest_framework import serializers, status
from rest_framework.authtoken.models import Token

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


class CountUserSerializer(serializers.Serializer):
    total_spec_user = serializers.SerializerMethodField()
    photo_user = serializers.SerializerMethodField()
    video_user = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'total_spec_user',
            'photo_user',
            'video_user',
        )

    def get_total_spec_user(self, services, *args, **kwargs):
        users = User.objects.filter(
            is_photographer=True
        ) | User.objects.filter(is_video_operator=True)
        return users.count()

    def get_photo_user(self, services, *args, **kwargs):
        return User.objects.filter(is_photographer=True).count()

    def get_video_user(self, services, *args, **kwargs):
        return User.objects.filter(is_video_operator=True).count()


class ServiceSerializer(serializers.ModelSerializer):
    image_service = Base64ImageField(required=False, allow_null=True)
    tag = TagsSerializer(read_only=True, many=True)
    authors = serializers.SerializerMethodField()
    due_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta:
        model = Service
        fields = (
            'authors',
            'name_service',
            'image_service',
            'cost_service',
            'description_service',
            'due_date',
            'order_delivery_time',
            'min_duration',
            'tag',
        )

    def get_authors(self, services, *args, **kwargs):
        authors = services.author.all()
        if authors is not None:
            return ShortUserSerializer(authors, many=True).data


class MediafileSerializer(serializers.ModelSerializer):
    authors = serializers.SerializerMethodField()
    photo = Base64ImageField(allow_null=True)

    class Meta:
        model = MediaFile
        fields = (
            'authors',
            'photo',
            'link',
            'title',
            'media_type',
            'is_main_photo',
        )
        read_only_fields = ('media_type',)

    def create(self, validated_data):
        authors = validated_data.get('authors')
        title = validated_data.get('title')
        image = validated_data.get('image')
        link = validated_data.get('link')
        is_main_photo = validated_data.get('is_main_photo')
        media_type = (
            MediaFile.MediaType.PHOTO.value
            if image
            else MediaFile.MediaType.VIDEO.value
        )
        media_file = MediaFile.objects.create(
            authors=authors,
            title=title,
            image=image,
            link=link,
            media_type=media_type,
            is_main_photo=is_main_photo,
        )
        return media_file

    def validate(self, attrs):
        image = attrs.get('image')
        video_link = attrs.get('link')
        if (image and video_link) or (not image and not video_link):
            raise serializers.ValidationError(
                detail='Укажите либо файл фотографии либо ссылку на видео',
                code=status.HTTP_400_BAD_REQUEST,
            )
        return super().validate(attrs)

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
            'equipment',
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


class SocialUserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = Token
        fields = ('token',)


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


class ShortServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('name_service',)


class GeneralCatalogSorting(serializers.Serializer):
    expert = serializers.CharField(max_length=200)
    isMaxCost = serializers.BooleanField()
    isMinCost = serializers.BooleanField()
    maxCost = serializers.CharField(max_length=250)
    minCost = serializers.CharField(max_length=250)
    typeOfShooting = ShortServiceSerializer(many=True, read_only=True)


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
