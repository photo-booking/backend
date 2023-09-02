from django.contrib import admin

from .models import Media_file, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'first_name',
        'last_name',
        'profile_photo',
        'email',
        'contact_email',
        'phone',
        'work_experience',
        'city',
        'raiting',
        'about_me',
        'is_client',
        'is_photographer',
        'is_video_operator',
        'birthday',
        'social_telegram',
        'social_vkontakte',
        'is_active',
    )
    search_fields = (
        'phone',
        'email',
        'city',
    )
    list_filter = (
        'phone',
        'email',
        'city',
        'work_experience',
        'is_client',
        'is_photographer',
        'is_video_operator',
    )
    empty_value_display = '-пусто-'


@admin.register(Media_file)
class Media_fileAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'link',
        'title',
        'media_type',
        'is_main_photo',
    )
    search_fields = (
        'title',
        'user',
    )
    list_filter = (
        'user',
        'media_type',
    )
    empty_value_display = '-пусто-'
