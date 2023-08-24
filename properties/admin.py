from django.contrib import admin

from properties.models import Feedback_property, Property, Room


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'name',
        'adress',
        'worktime',
        'area',
        'price',
    )
    search_fields = (
        'user',
        'name',
        'adress',
        'worktime',
        'area',
        'price',
    )
    list_filter = (
        'worktime',
        'price',
        'area',
        'user',
    )


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        'property',
        'name',
        'area',
        'price',
    )
    search_fields = ('property', 'name', 'adress', 'area', 'price')
    list_filter = (
        'price',
        'area',
    )


@admin.register(Feedback_property)
class FBpropertyAdmin(admin.ModelAdmin):
    list_display = ('property', 'raiting', 'descriptions', 'user_client')
    search_fields = (
        'property',
        'raiting',
        'user_client',
    )
    list_filter = (
        'property',
        'user_client',
    )
