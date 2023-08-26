from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from phone_field import PhoneField

from services.models import Service
from users.validators import CorrectUsernameAndNotMe


class User(AbstractUser):
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=settings.MAX_LEN_NAME,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=settings.MAX_LEN_NAME,
    )
    username = models.CharField(
        ("username"),
        max_length=150,
        unique=True,
        validators=[CorrectUsernameAndNotMe],
    )
    profile_photo = models.ImageField(
        verbose_name='Фото профиля',
        upload_to='users/profile',
        blank=True
    )
    email = models.EmailField(
        verbose_name='Почта для регистрации',
        unique=True
    )
    contact_email = models.EmailField(
        verbose_name='Почта для связи',
        blank=True,
        null=True
    )
    phone = PhoneField(
        verbose_name='Номер телефона',
        unique=True,
        help_text='Телефон для контакта'

    )
    servicies = models.ManyToManyField(
        Service,
        verbose_name='Услуги',
        related_name='users',
    )
    work_experience = models.FloatField(
        verbose_name='Опыт работы',
        default=0,
    )
# Нужно сделать базу с городами
    city = models.CharField(
        verbose_name='Город',
        help_text='Укажите город проживания',
        max_length=settings.MAX_LEN_NAME
    )
    raiting = models.PositiveSmallIntegerField(
        verbose_name='Рейтинг профиля',
        blank=True,
        null=True,
    )
    about_me = models.TextField(
        verbose_name='Обо мне',
        max_length=settings.MAX_TEXT_LEN
    )
    is_photographer = models.BooleanField(
        verbose_name='Роль.Фотограф',
        default=False
    )
    is_video_operator = models.BooleanField(
        verbose_name='Роль.Видео-оператор',
        default=False
    )
    birthday = models.DateField(
        verbose_name='День рождения',
        blank=True,
        null=True
    )
    social = models.URLField(
        verbose_name='Социальные сети',
        blank=True,
        null=True
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'username',
        'first_name',
        'last_name',
        'phone',
    )

    class Meta:
        ordering = ('email',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class MediaFile(models.Model):
    link = models.URLField(
        verbose_name='Ссылка на медиа файл'
    )
    title = models.CharField(
        verbose_name='Название',
        max_length=settings.MAX_LEN_NAME
    )
    media_type = models.CharField(
        verbose_name='Тип медиа файла',
        max_length=settings.MAX_LEN_NAME
    )
    is_main_photo = models.BooleanField(
        verbose_name='Отображение файла на главной'
    )

    class Meta:
        verbose_name = 'Медиа файл'
        verbose_name_plural = 'Медиа файлы'

    def __str__(self):
        return self.title
