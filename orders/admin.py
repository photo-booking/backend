from django.contrib import admin

from .models import Order, Raiting


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    model = Order
    filter_horizontal = ('users',)
    list_display = (
        'name',
        'cost',
        'date',
        'completion_date',
        'status',
        'service',
        'chat',
    )
    search_fields = (
        'name',
        'cost',
        'date',
        'status',
        'users',
        'service',
    )
    list_filter = (
        'name',
        'cost',
        'date',
        'status',
        'users',
        'service',
    )
    empty_value_display = '-пусто-'


@admin.register(Raiting)
class RaitingAdmin(admin.ModelAdmin):
    model = Raiting
    filter_horizontal = ('user',)
    list_display = (
        'order',
        'raiting',
    )
    search_fields = ('user', 'order')
    list_filter = (
        'order',
        'user',
    )
    empty_value_display = '-пусто-'
