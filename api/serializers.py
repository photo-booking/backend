from django.conf import settings
from rest_framework import serializers
from users.models import User
from users.validators import CorrectUsernameAndNotMe


class UserSerializer(serializers.ModelSerializer, CorrectUsernameAndNotMe):
    is_subscribed = serializers.SerializerMethodField()
    email = serializers.EmailField(
        required=True,
        max_length=settings.MAX_EMAIL_NAME_LENGTH
    )
    first_name = serializers.CharField(
        required=True,
        max_length=settings.MAX_LEN_NAME
    )
    last_name = serializers.CharField(
        required=True,
        max_length=settings.MAX_LEN_NAME
    )

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'password',
        )
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ('is_subscribed',)
