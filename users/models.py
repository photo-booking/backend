from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from phone_field import PhoneField

from users.validators import CorrectUsernameAndNotMe


class Service(models.Model):
    name_service = models.CharField(
        verbose_name='Название услуги',
        max_length=settings.MAX_LEN_NAME
    )
    image_service = models.ImageField(
        verbose_name='Фотография услуги',
        upload_to='users/tags',
        blank=True,
    )
    cost_service = models.PositiveIntegerField(
        verbose_name='Стоимость услуги'
    )
    description_service = models.TextField(
        verbose_name='Описание услуги',
        max_length=settings.MAX_LEN_NAME
    )
    due_date = models.DateTimeField(
        verbose_name='Срок выполнения'
    )
    equipment = models.CharField(
        verbose_name='Оборудование',
        max_length=settings.MAX_LEN_NAME
    )

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    def __str__(self):
        return self.name_service


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
        'Почта',
        unique=True
    )
    phone = PhoneField(
        verbose_name='Номер телефона',
        unique=True,
        help_text='Телефон для контакта'

    )
    service = models.ManyToManyField(
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
        'city'
    )

    class Meta:
        ordering = ('email',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Property(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Владелец недвижимости',
        related_name='properties',
        on_delete=models.CASCADE,
        null=True
    )
    name = models.CharField(
        verbose_name='Название недвижимости',
        max_length=settings.MAX_LEN_NAME
    )
    adress = models.CharField(
        verbose_name='Адрес',
        max_length=settings.MAX_LEN_NAME
    )
    worktime = models.TextField(
        verbose_name='Время работы'
    )
    area = models.FloatField(
        verbose_name='Общая площадь помещений'
    )
    price = models.FloatField(
        verbose_name='Стоимость помещений'
    )

    class Meta:
        verbose_name = 'Недвижимость'
        verbose_name_plural = 'Недвижимость'

    def __str__(self):
        return self.name


class Room(models.Model):
    property = models.ForeignKey(
        Property,
        verbose_name='Номер комнаты',
        related_name='rooms',
        on_delete=models.CASCADE,
        null=True
    )
    name = models.CharField(
        verbose_name='Название помещния',
        max_length=settings.MAX_LEN_NAME
    )
    area = models.FloatField(
        verbose_name='Площадь помещения'
    )
    price = models.FloatField(
        verbose_name='Стоимость помещения'
    )


class Feedback_property(models.Model):
    raiting = models.PositiveSmallIntegerField(
        verbose_name='Рейтинг предприятия',
        blank=True
    )
    descriptions = models.CharField(
        verbose_name='Текст обратной связи',
        max_length=settings.MAX_TEXT_LEN
    )
    user_client = models.ForeignKey(
        User,
        verbose_name='Клиент',
        related_name='feedback_properties',
        on_delete=models.CASCADE,
        null=True
    )
    property = models.ForeignKey(
        Property,
        verbose_name='Название недвижимости',
        related_name='feedback_properties',
        on_delete=models.CASCADE,
        null=True
    )

    class Meta:
        verbose_name = 'Обратная связь'

    def __str__(self):
        return self.raiting
