from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from api import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(urls)),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )


schema_view = get_schema_view(
    openapi.Info(
        title="photo-market API",
        default_version='v1',
        description="Документация для приложения photo-market",
        # terms_of_service="URL страницы с пользовательским соглашением",
        contact=openapi.Contact(email="german220515@yandex.ru"),
        license=openapi.License(name="BSD License"),
    ),
    url='https://photo-market.acceleratorpracticum.ru/api/',
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    re_path(
        r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json',
    ),
    re_path(
        r'^swagger/$',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui',
    ),
    re_path(
        r'^redoc/$',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc',
    ),
]
