from django.conf import settings
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
    class ServiceTypes(enums.Choices):
        PHOTO = 'Фотосъемка'
        VIDEO = 'Видеосъемка'

        @classmethod
        def choices(cls):
            return [(key.name, key.value) for key in cls]

    author = models.ForeignKey(
        'users.User',
        verbose_name='Автор',
        on_delete=models.CASCADE,
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
    due_date = models.DateTimeField(verbose_name='Срок выполнения')
    tag = models.ManyToManyField(
        Tag, verbose_name='Вид съемки', blank=True, related_name='services'
    )
    service_type = models.CharField(
        verbose_name='Тип услуги',
        choices=ServiceTypes.choices,
        blank=True,
        help_text='Фото или Видеосъемка',
    )

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    def __str__(self):
        return self.name_service


class MediaFile(models.Model):
    class MediaTypeEnum(enums.Choices):
        VIDEO = 'VIDEO'
        PHOTO = 'PHOTO'

        @classmethod
        def choices(cls):
            return [(key.name, key.value) for key in cls]

    title = models.CharField(
        verbose_name='Название', max_length=settings.MAX_LEN_NAME
    )
    video_link = models.URLField(
        verbose_name='Ссылка на медиа файл',
        blank=True,
        null=True,
    )
    image = models.ImageField(
        verbose_name='Фотография',
        upload_to='users/images',
        blank=True,
        null=True,
    )
    media_type = models.CharField(
        verbose_name='Тип медиа файла',
        choices=MediaTypeEnum.choices,
    )
    is_main_photo = models.BooleanField(
        verbose_name='Отображение файла на главной'
    )
    service = models.ForeignKey(
        'services.Service',
        on_delete=models.CASCADE,
        related_name='media_files',
    )

    def save(self, *args, **kwargs):
        if self.image and self.video_link:
            raise ValueError('Выберите только один тип медиа')
        if self.image:
            self.media_type = MediaFile.MediaTypeEnum.PHOTO.value
        else:
            self.media_type = MediaFile.MediaTypeEnum.VIDEO.value
        super(MediaFile, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Медиа файл'
        verbose_name_plural = 'Медиа файлы'
        constraints = (
            models.CheckConstraint(
                check=models.Q(image__exact='')
                | models.Q(video_link__exact=''),
                name='Только один вид медиа',
            ),
        )

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
