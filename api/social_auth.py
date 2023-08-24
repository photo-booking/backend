# import requests
# from django.conf import settings
# from django.contrib.auth import REDIRECT_FIELD_NAME, login
# from django.shortcuts import redirect

# from users.models import User


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
