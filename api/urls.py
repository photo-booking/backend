from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    ChatViewSet,
    FBpropertyViewSet,
    GeneralCatalogExecutorCardViewSet,
    MediafileViewSet,
    MessageViewSet,
    OrderViewSet,
    PropertyViewSet,
    RaitingViewSet,
    RoomViewSet,
    ServiceViewSet,
    UserViewSet,
    count_user,
    get_token_user_from_google,
    get_token_from_vk_user,
)

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, 'users')
router_v1.register('properties', PropertyViewSet, 'properties')
router_v1.register('rooms', RoomViewSet, 'rooms')
router_v1.register('feedback_property', FBpropertyViewSet, 'feedback_property')
router_v1.register('services', ServiceViewSet, 'services')
router_v1.register('catalog', GeneralCatalogExecutorCardViewSet, 'catalog')
router_v1.register('orders', OrderViewSet, 'orders')
router_v1.register('chats', ChatViewSet, 'chats')
router_v1.register('messages', MessageViewSet, 'messages')
router_v1.register('media_files', MediafileViewSet, 'media_files')
router_v1.register('raitings', RaitingViewSet, 'raitings')

urlpatterns = (
    path('users/count/', count_user, name='count_user'),
    path('', include(router_v1.urls)),
    path('auth/', include('djoser.urls.authtoken')),
    path('social_google/', get_token_user_from_google, name='google'),
    path('social_vk/', get_token_from_vk_user, name='vk')
)
