from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    ChatViewSet,
    FBpropertyViewSet,
    MediafileViewSet,
    MessageViewSet,
    OrderViewSet,
    PropertyViewSet,
    RaitingViewSet,
    RoomViewSet,
    ServiceViewSet,
    UserViewSet,
    index
)

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, 'users')
router_v1.register('properties', PropertyViewSet, 'properties')
router_v1.register('rooms', RoomViewSet, 'rooms')
router_v1.register('feedback_property', FBpropertyViewSet, 'feedback_property')
router_v1.register('services', ServiceViewSet, 'services')
router_v1.register('orders', OrderViewSet, 'orders')
router_v1.register('chats', ChatViewSet, 'chats')
router_v1.register('messages', MessageViewSet, 'messages')
router_v1.register('media_files', MediafileViewSet, 'media_files')
router_v1.register('raitings', RaitingViewSet, 'raitings')

urlpatterns = (
    path('', include(router_v1.urls)),
    path('auth/', include('djoser.urls.authtoken')),
    path('social/', include('social_django.urls', namespace="social")),
    path('main/', index),
)
