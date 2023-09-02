from rest_framework import serializers

from orders.models import Chat, Message, Order, Raiting
from properties.models import Feedback_property, Property, Room
from services.models import Service
from users.models import Media_file, User


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


class MediafileSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field='id')

    class Meta:
        model = Media_file
        fields = (
            'user',
            'link',
            'title',
            'media_type',
            'is_main_photo',
        )


class UserSerializer(serializers.ModelSerializer):
    servicies = ServiceSerializer(
        many=True,
    )
    media_file = serializers.SerializerMethodField()

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
            'servicies',
            'media_file',
        )

    def get_media_file(self, user, *args, **kwargs):
        foto = user.media_file_set.all()
        if foto is not None:
            return MediafileSerializer(foto, many=True).data


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
        model = Feedback_property
        fields = (
            'property',
            'raiting',
            'descriptions',
            'user_client',
        )


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
