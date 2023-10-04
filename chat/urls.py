from django.urls import path

from .views import index, room

app_name = 'chat'


urlpatterns = [
    #    path('test/', views.test),
    path('', index, name='index'),
    path('room/<int:pk>/', room, name='room'),
]
