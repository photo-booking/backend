from djoser.views import UserViewSet as DjoserUserViewSet

from api.paginators import LimitPageNumberPagination
from users.models import User


class UserViewSet(DjoserUserViewSet):
    queryset = User.objects.all()
    pagination_class = LimitPageNumberPagination
