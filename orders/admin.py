from django.contrib import admin

from .models import Order, Raiting


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = (
        'name',
        'cost',
        'date',
        'completion_date',
        'status',
        'service',
        'customer_user',
        'executor_user',
    )
    search_fields = (
        'name',
        'cost',
        'date',
        'status',
        'customer_user',
        'executor_user',
        'service',
    )
    list_filter = (
        'name',
        'cost',
        'date',
        'status',
        'customer_user',
        'executor_user',
        'service',
    )
    empty_value_display = '-пусто-'


@admin.register(Raiting)
class RaitingAdmin(admin.ModelAdmin):
    model = Raiting
    list_display = (
        'order',
        'raiting',
        'customer_user',
        'executor_user',
    )
    search_fields = ('executor_user', 'order')
    list_filter = (
        'order',
        'executor_user',
    )
    empty_value_display = '-пусто-'
