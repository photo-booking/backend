from rest_framework import serializers

from properties.models import Feedback_property, Property, Room
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
        model = Feedback_property
        fields = (
            'property',
            'raiting',
            'descriptions',
            'user_client',
        )
