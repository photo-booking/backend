from rest_framework.pagination import PageNumberPagination


class LimitPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    page_size = 20


class PortfolioLimitPageNumberPagination(LimitPageNumberPagination):
    page_size_query_param = 'limit'
    page_size = 3
