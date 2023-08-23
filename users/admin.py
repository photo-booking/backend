from django.contrib import admin

from .models import User


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
