from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import FBpropertyViewSet, PropertyViewSet, RoomViewSet, UserViewSet

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, 'users')
router_v1.register('properties', PropertyViewSet, 'properties')
router_v1.register('rooms', RoomViewSet, 'rooms')
router_v1.register('feedback_property', FBpropertyViewSet, 'feedback_property')


urlpatterns = (
    path('', include(router_v1.urls)),
    path('auth/', include('djoser.urls.authtoken')),
)
