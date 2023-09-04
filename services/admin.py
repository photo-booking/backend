from django.contrib import admin

from .models import MediaFile, Service, Tag


class MediaFileInline(admin.TabularInline):
    model = MediaFile


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        'name_service',
        'image_service',
        'cost_service',
        'description_service',
        'due_date',
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
    inlines = (MediaFileInline,)
    empty_value_display = '-пусто-'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


@admin.register(MediaFile)
class MediaFileAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'image',
        'video_link',
        'media_type',
        'is_main_photo',
        'service',
    )
    readonly_fields = ('media_type',)
