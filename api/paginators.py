from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class LimitPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    page_size = 20


class CatalogPagination(LimitPageNumberPagination):
    page_size = 15


class ServicePagination(LimitPageNumberPagination):
    page_size = 6

    def get_paginated_response(self, data, expert):
        return Response(
            OrderedDict(
                [
                    ('count', self.page.paginator.count),
                    ('next', self.get_next_link()),
                    ('previous', self.get_previous_link()),
                    ('expert', expert),
                    ('results', data),
                ]
            )
        )
