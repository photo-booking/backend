from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import viewsets

from api.paginators import LimitPageNumberPagination
from properties.models import Feedback_property, Property, Room
from users.models import User

from .serializers import (
    FBpropertySerializer,
    PropertySerializer,
    RoomSerializer,
)


class UserViewSet(DjoserUserViewSet):
    queryset = User.objects.all()
    pagination_class = LimitPageNumberPagination


class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class FBpropertyViewSet(viewsets.ModelViewSet):
    queryset = Feedback_property.objects.all()
    serializer_class = FBpropertySerializer
