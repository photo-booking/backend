import django_filters

# from django.contrib.auth import get_user_model
from rest_framework.filters import SearchFilter

# from orders.models import Chat, Message, Order, Raiting
# from properties.models import Feedback_property, Property, Room
# from services.models import Service
from users.models import User


class СontractorFilter(SearchFilter):
    search_param = 'first_name'


class UsersFilter(django_filters.FilterSet):
    is_photographer = django_filters.BooleanFilter(
        method='filter_is_photographer'
    )
    is_video_operator = django_filters.BooleanFilter(
        method='filter_is_video_operator'
    )
    tags = django_filters.AllValuesMultipleFilter(
        field_name='services__name_service'
    )
    user = django_filters.ModelChoiceFilter(queryset=User.objects.all())

    class Meta:
        model = User
        fields = ('tags', 'user', 'is_photographer', 'is_video_operator')

    def filter_is_photographer(self, queryset, name, value):
        print(999)
        if value and self.request.user.is_authenticated:
            return queryset.filter(is_photographer=True)
        return queryset

    def filter_is_video_operator(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(is_video_operator=True)
        return queryset
