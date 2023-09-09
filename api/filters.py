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
    spec = django_filters.BooleanFilter(
        method='filter_spec',
        label='укажите photographer или videographer или all',
    )
    max_cost = django_filters.BooleanFilter(
        method='filter_max_cost', label='укажите max_cost bool'
    )
    min_cost = django_filters.BooleanFilter(
        method='filter_min_cost', label='укажите min_cost bool'
    )
    minCost = django_filters.BooleanFilter(
        method='filter_minCost',
        label='укажите minCost int',
    )
    maxCost = django_filters.BooleanFilter(
        method='filter_maxCost', label='укажите maxCost int'
    )
    user__services = django_filters.CharFilter(
        field_name='services__name_service',
        lookup_expr='contains',
        label='Отфильтруйте по услуге (например Babyfoto)',
    )

    class Meta:
        model = User
        fields = (
            'user__services',
            'spec',
            'max_cost',
            'max_cost',
            'minCost',
            'maxCost',
        )

    def filter_spec(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            queryset = queryset.filter(
                is_video_operator=True
            ) | queryset.filter(is_video_operator=True)
            return queryset

    def filter_max_cost(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            queryset = queryset.order_by('services__cost_service')
            return queryset

    def filter_min_cost(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            queryset = queryset.order_by('-services__cost_service')
            return queryset

    def filter_minCost(self, queryset, name, value):
        if value:
            return queryset.filter(
                services__cost_service__range=(
                    self.kwargs['minCost'],
                    self.kwargs['maxCost'],
                )
            )

    def filter_maxCost(self, queryset, name, value):
        if value:
            return queryset.filter(
                services__cost_service__range=(
                    self.kwargs['minCost'],
                    self.kwargs['maxCost'],
                )
            )
