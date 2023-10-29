from rest_framework.pagination import PageNumberPagination


class LimitPageNumberPagination(PageNumberPagination):
    page_query_param = 'limit'
    page_size_query_param = 'page_size'
    page_size = 20


class ReviewsPageNumberPagination(LimitPageNumberPagination):
    page_size = 6


class PortfolioLimitPageNumberPagination(LimitPageNumberPagination):
    page_query_param = 'limit'
    page_size = 3


class CatalogPagination(LimitPageNumberPagination):
    page_size = 15
