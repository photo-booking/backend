from rest_framework import serializers

from users.models import User
from users.validators import CorrectUsernameAndNotMe


class UserSerializer(serializers.ModelSerializer, CorrectUsernameAndNotMe):
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
