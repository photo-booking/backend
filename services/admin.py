from django.contrib import admin

from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        'name_service',
        'image_service',
        'cost_service',
        'description_service',
        'due_date',
        'equipment',
    )
    search_fields = (
        'cost_service',
        'due_date',
        'name',
    )
    list_filter = (
        'cost_service',
        'due_date',
    )
    empty_value_display = '-пусто-'
