"""
ASGI config for photo_booking project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""


import os

import django

# from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

# from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

from chat import routing
from chat.middleware import JwtAuthMiddlewareStack

# from chat.middleware import JwtAuthMiddlewareStack

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "photo_booking.settings")
django.setup()

# application = get_asgi_application()

# application = ProtocolTypeRouter({
#         "http": get_asgi_application(),
#         'websocket': AllowedHostsOriginValidator(
#             AuthMiddlewareStack(
#                 URLRouter(routing.websocket_urlpatterns)
#             )
#         ),
# })

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": JwtAuthMiddlewareStack(
            URLRouter(routing.websocket_urlpatterns)
        ),
    }
)
