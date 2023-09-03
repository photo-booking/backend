from django.contrib import admin

from .models import MediaFile, Service


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


@admin.register(MediaFile)
class MediaFileAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'author',
        'service',
        'link',
        'title',
        'media_type',
        'is_main_photo',
    )
    search_fields = (
        'title',
        'service',
        'author',
    )
    list_filter = ('media_type',)
    empty_value_display = '-пусто-'

    def author(self, obj):
        return ', '.join([author.pk for author in obj.mediafile.all()])

    def service(self, obj):
        return ', '.join(
            [service.name_service for service in obj.service_set.all()]
        )
