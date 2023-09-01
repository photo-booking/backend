from django_filters import rest_framework as filters, OrderingFilter

from users.models import User


class CatalogFilter(filters.FilterSet):
    services = filters.AllValuesMultipleFilter(
        field_name='services__name_service')
    is_photographer = filters.BooleanFilter()
    is_video_operator = filters.BooleanFilter()
    price = filters.NumberFilter(field_name='services__cost_service')
    min_price = filters.NumberFilter(
        field_name='services__cost_service', lookup_expr='gte')
    max_price = filters.NumberFilter(
        field_name='services__cost_service', lookup_expr='lte')

    ordering = OrderingFilter(
        choices=(
            ('price', 'Price'),
        ),
        fields={
            'services__cost_service': 'price',
        }
    )

    class Meta:
        model = User
        fields = ['services', 'is_photographer',
                  'is_video_operator', 'price', ]
