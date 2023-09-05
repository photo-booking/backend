# import requests
# from django.conf import settings
# from django.contrib.auth import REDIRECT_FIELD_NAME, login
# from django.shortcuts import redirect
import http

from djoser.views import TokenCreateView
from rest_framework.decorators import api_view
# from users.models import User
from rest_framework.response import Response
from rest_framework.views import APIView

# def get_vk_token(code):
#     client_id = settings.VK_APP_ID
#     client_secret = settings.VK_APP_SECRET
#     url = f''
#     request = requests.get(url=url)
#     data = request.json()
#     return data


# def check_email_in_bd(email):
#     if User.objects.filter(email=email).exists():
#         url = 'http://127.0.0.1:8000/'
#         return redirect(url)


from social_django.strategy import DjangoStrategy


def get_drf_token(user):
    token = TokenCreateView(user)
    return token


@api_view(['GET', ])
def post_token(request):
    token = get_drf_token(request.user)
    return Response({'token': f',kzzz{token}'}, status=http.HTTPStatus.OK)


class CustomStrategy(DjangoStrategy):
    def get_setting(self, name):
        if name == 'LOGIN_REDIRECT_URL':
            return f'/api/google-oauth2'
        else:
            return super().get_setting(name)
