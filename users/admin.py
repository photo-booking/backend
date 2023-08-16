from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'first_name',
                    'last_name',
                    'email',
                    'phone',
                    'work_experience',
                    'city',
                    'raiting',
                    'about_me',
                    'is_photographer',
                    'is_video_operator',
                    'birthday',
                    'social',
                    )
    search_fields = ('phone', 'email', 'city',)
    list_filter = ('phone', 'email', 'city',)
    empty_value_display = '-пусто-'
