from django.conf import settings
from rest_framework import serializers

from users.models import User
from users.validators import CorrectUsernameAndNotMe


class UserSerializer(serializers.ModelSerializer, CorrectUsernameAndNotMe):
    first_name = serializers.CharField(
        required=True,
        max_length=settings.MAX_LEN_NAME
    )
    last_name = serializers.CharField(
        required=True,
        max_length=settings.MAX_LEN_NAME
    )
    username = serializers.CharField()
    email = serializers.EmailField(
        required=True,
        max_length=settings.MAX_EMAIL_NAME_LENGTH
    )
    phone = serializers.CharField()
    work_experience = serializers.CharField()
    city = serializers.CharField()
    raiting = serializers.CharField()
    about_me = serializers.CharField()
    is_photographer = serializers.BooleanField()
    is_video_operator = serializers.BooleanField()
    birthday = serializers.DateField()
    social = serializers.CharField()

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'phone',
            'work_experience',
            'city',
            'raiting',
            'about_me',
            'is_photographer',
            'is_video_operator',
            'birthday',
            'social',
        )
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ('is_subscribed',)
