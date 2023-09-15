from django.contrib import admin

from .models import MediaFile, MediaService, Service, Tag


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        'name_service',
        'image_service',
        'cost_service',
        'description_service',
        'due_date',
        'min_duration',
        'tag',
    )
    search_fields = (
        'cost_service',
        'due_date',
        'name',
    )
    list_filter = ('cost_service',)
    empty_value_display = '-пусто-'

    def tag(self, obj):
        return ', '.join([tag.services.pk for tag in obj.services.all()])


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug',
    )
    search_fields = (
        'pk',
        'slug',
        'name',
    )


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
            [
                service.service.name_service
                for service in obj.media_services.all()
            ]
        )


@admin.register(MediaService)
class MediaServiceAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'service',
        'media_file',
    )
    search_fields = ('pk',)
