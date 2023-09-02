from rest_framework import serializers

from orders.models import Chat, Message, Order, Raiting
from properties.models import FeedbackProperty, Property, Room
from services.models import Service, MediaFile
from users.models import User


class UserSerializer(serializers.ModelSerializer):
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
        )


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


class MediafileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaFile
        fields = (
            'link',
            'title',
            'media_type',
            'is_main_photo',
        )


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = (
            'name_service',
            'image_service',
            'cost_service',
            'description_service',
            'due_date',
            'equipment',
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
