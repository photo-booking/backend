from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from phone_field import PhoneField

from users.validators import CorrectEmail, CorrectUsernameAndNotMe


class Tag(models.Model):
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
    description_service = models.CharField(
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
#   author_id = models.ForeignKey(User)

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    def __str__(self):
        return self.name_service


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name')
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
        unique=True,
        validators=[CorrectEmail],
    )
    phone = PhoneField(
        verbose_name='Номер телефона',
        unique=True,
        help_text='Телефон для контакта'

    )
    tag_id = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
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
    raiting = models.IntegerField(
        verbose_name='Рейтинг профиля',
        blank=True,
        null=True,
    )
    about_me = models.CharField(
        verbose_name='Обо мне',
        max_length=settings.MAX_TEXT_LEN
    )
    is_photographer = models.BooleanField(
        verbose_name='Роль. Фотограф',
        default=False
    )
    is_video_operator = models.BooleanField(
        verbose_name='Роль. Видео оператор',
        default=False
    )
    birthday = models.DateField(
        verbose_name='День рождения',
        blank=True,
        null=True
    )
    social = models.CharField(
        verbose_name='Социальные сети',
        blank=True,
        max_length=settings.MAX_LEN_NAME,
        null=True
    )

    class Meta:
        ordering = ('email',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Property(models.Model):
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
    property_id = models.ForeignKey(
        User,
        verbose_name='Номер недвижимости',
        related_name='properties',
        on_delete=models.CASCADE,
        null=True
    )

    class Meta:
        verbose_name = 'Недвижимость'
        verbose_name_plural = 'Недвижимость'

    def __str__(self):
        return self.name


class Feedback_property(models.Model):
    raiting = models.IntegerField(
        verbose_name='Рейтинг предприятия',
        blank=True
    )
    descriptions = models.CharField(
        verbose_name='Текст обратной связи',
        max_length=settings.MAX_TEXT_LEN
    )
    user_client_id = models.ForeignKey(
        User,
        verbose_name='ФИО клиента',
        related_name='feedback_properties',
        on_delete=models.CASCADE,
        null=True
    )
    feedback_id = models.ForeignKey(
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
