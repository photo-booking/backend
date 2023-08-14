from api.paginators import LimitPageNumberPagination
from djoser.views import UserViewSet as DjoserUserViewSet
from users.models import User


class UserViewSet(DjoserUserViewSet):
    queryset = User.objects.all()
    pagination_class = LimitPageNumberPagination
