from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import enums


class Tag(models.Model):
    name = models.CharField(
        max_length=settings.MAX_LEN_NAME,
        db_index=True,
        verbose_name='имя',
        unique=True,
    )
    slug = models.SlugField('Индификатор', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Service(models.Model):
    author = models.ManyToManyField(
        'users.User',
        verbose_name='Автор',
        related_name='services',
    )
    name_service = models.CharField(
        verbose_name='Название услуги', max_length=settings.MAX_LEN_NAME
    )
    image_service = models.ImageField(
        verbose_name='Фотография услуги',
        upload_to='users/tags',
        blank=True,
    )
    cost_service = models.PositiveIntegerField(verbose_name='Стоимость услуги')
    description_service = models.TextField(
        verbose_name='Описание услуги', max_length=settings.MAX_LEN_NAME
    )
    due_date = models.DateTimeField(verbose_name='Начало выполнения')
    order_delivery_time = models.PositiveSmallIntegerField(
        editable=True,
        verbose_name='Срок выполнения',
        help_text='введите срок предоставления'
        'обработаных фотографий в днях',
        validators=[MinValueValidator(1, 'минимальное значение 1')],
    )
    min_duration = models.PositiveSmallIntegerField(
        editable=True,
        verbose_name='Минимальное время съемки в часах',
        help_text='введите время съемки в часах',
        validators=[MinValueValidator(1, 'минимальное значение 1')],
    )
    tag = models.ManyToManyField(
        Tag, verbose_name='Вид съемки', blank=True, related_name='services'
    )

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    def __str__(self):
        return self.name_service


class MediaFile(models.Model):
    class MediaType(enums.Choices):
        VIDEO = 'VIDEO'
        PHOTO = 'PHOTO'

        @classmethod
        def choices(cls):
            return [(key.name, key.value) for key in cls]

    author = models.ForeignKey(
        'users.User',
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='mediafiles',
    )
    link = models.URLField(verbose_name='Ссылка на видео', blank=True)
    title = models.CharField(
        verbose_name='Название', max_length=settings.MAX_LEN_NAME
    )
    photo = models.ImageField(
        verbose_name='Фотография', upload_to='users/photos', blank=True
    )
    media_type = models.CharField(
        verbose_name='Тип медиа файла',
        choices=MediaType.choices,
        max_length=settings.MAX_LEN_NAME,
    )
    is_main_photo = models.BooleanField(
        verbose_name='Отображение файла на главной'
    )

    class Meta:
        verbose_name = 'Медиа файл'
        verbose_name_plural = 'Медиа файлы'
        constraints = (
            models.CheckConstraint(
                check=models.Q(photo__exact='') | models.Q(link__exact=''),
                name='Укажите только один вид медиа',
            ),
        )

    def save(self, *args, **kwargs):
        if self.photo:
            self.media_type = MediaFile.MediaType.PHOTO.value
        else:
            self.media_type = MediaFile.MediaType.VIDEO.value
        super(MediaFile, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Portfolio(models.Model):
    author = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        blank=False,
        related_name='portfolio',
    )
    media_file = models.ForeignKey(MediaFile, on_delete=models.CASCADE)


class MediaService(models.Model):
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        blank=False,
        related_name='media_services',
    )
    media_file = models.ForeignKey(
        MediaFile,
        on_delete=models.CASCADE,
        blank=False,
        related_name='media_services',
    )
