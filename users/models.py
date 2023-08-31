from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from phone_field import PhoneField

from services.models import Service


class AccountManager(BaseUserManager):
    def create_user(self, email, first_name='default', last_name='defaul',
                    password=None, is_client=True):
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            is_client=is_client,
        )
        user.set_password(password)
        user.is_staff = False
        user.is_superuser = False
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email, first_name, last_name, password, is_client
    ):
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            is_client=is_client,
        )
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, email_):
        return self.get(email=email_)


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=settings.MAX_LEN_NAME,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=settings.MAX_LEN_NAME,
    )
    profile_photo = models.ImageField(
        verbose_name='Фото профиля', upload_to='users/profile', blank=True
    )
    email = models.EmailField(
        verbose_name='Почта для регистрации', unique=True
    )
    contact_email = models.EmailField(
        verbose_name='Почта для связи', blank=True, null=True
    )
    phone = PhoneField(
        verbose_name='Номер телефона',
        help_text='Телефон для контакта',
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
        max_length=settings.MAX_LEN_NAME,
    )
    raiting = models.PositiveSmallIntegerField(
        verbose_name='Рейтинг профиля',
        blank=True,
        null=True,
    )
    about_me = models.TextField(
        verbose_name='Обо мне', max_length=settings.MAX_TEXT_LEN
    )
    is_client = models.BooleanField(verbose_name='Роль.Клиент', default=True)
    is_photographer = models.BooleanField(
        verbose_name='Роль.Фотограф', default=False
    )
    is_video_operator = models.BooleanField(
        verbose_name='Роль.Видео-оператор', default=False
    )
    birthday = models.DateField(
        verbose_name='День рождения', blank=True, null=True
    )
    social_telegram = models.URLField(
        verbose_name='Телеграм', blank=True, null=True
    )
    social_vkontakte = models.URLField(
        verbose_name='Вконтакте', blank=True, null=True
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'first_name',
        'last_name',
        'is_client',
    )

    objects = AccountManager()

    def get_short_name(self):
        return self.email

    def natural_key(self):
        return self.email

    class Meta:
        ordering = ('email',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email


class Media_file(models.Model):
    link = models.URLField(verbose_name='Ссылка на медиа файл')
    title = models.CharField(
        verbose_name='Название', max_length=settings.MAX_LEN_NAME
    )
    media_type = models.CharField(
        verbose_name='Тип медиа файла', max_length=settings.MAX_LEN_NAME
    )
    is_main_photo = models.BooleanField(
        verbose_name='Отображение файла на главной'
    )

    class Meta:
        verbose_name = 'Медиа файл'
        verbose_name_plural = 'Медиа файлы'

    def __str__(self):
        return self.title
