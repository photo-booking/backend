import os

import django

# import jwt
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware

# from channels.auth import AuthMiddlewareStack
# from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token

# from datetime import datetime


# from users.models import User

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

ALGORITHM = "HS256"


@database_sync_to_async
def get_user(token):
    try:
        user = get_object_or_404(Token, key=token).user
        # payload = jwt.decode(token, settings.SECRET_KEY,
        # algorithms=ALGORITHM)
        # print('payload', payload)
        print('payload', user)
    except Exception:
        print('no payload')
        return AnonymousUser()

    # token_exp = datetime.fromtimestamp(payload['exp'])
    # if token_exp < datetime.utcnow():
    #     print("no date-time")
    #     return AnonymousUser()

    # try:
    #     user = User.objects.get(id=payload['user_id'])
    #     print('user', user)
    # except User.DoesNotExist:
    #     print('no user')
    #     return AnonymousUser()
    return user


class TokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        close_old_connections()
        # token_key = scope['query_string'].decode().split('=')[-1]
        # try:
        #     token_key = (
        #         dict(
        #             (
        #                 x.split('=')
        #                 for x in scope['query_string'].decode().split("&")
        #             )
        #         )
        #     ).get('token', None)
        # except ValueError:
        #     token_key = None
        try:
            token_key = (
                dict(scope['headers'])[b'authorization']
                .decode('utf-8')
                .split(" ")[1]
            )
            print('d1', token_key)
        except ValueError:
            token_key = None

        scope['user'] = await get_user(token_key)
        print(token_key)
        print('d2', scope['user'])
        return await super().__call__(scope, receive, send)


def JwtAuthMiddlewareStack(inner):
    return TokenAuthMiddleware(inner)
    # return TokenAuthMiddleware(AuthMiddlewareStack(inner))
