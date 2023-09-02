from django.conf import settings
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=settings.MAX_LEN_NAME, db_index=True,
                            verbose_name='имя',
                            unique=True)
    slug = models.SlugField('Индификатор', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Service(models.Model):
    author = models.ForeignKey(
        'users.User',
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='services'
    )
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
    tag = models.ManyToManyField(
        Tag,
        verbose_name='Вид съемки',
        blank=True,
        related_name='services'
    )

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    def __str__(self):
        return self.name_service


class MediaFile(models.Model):
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


class Portfolio(models.Model):
    author = models.ForeignKey('users.User',
                               on_delete=models.CASCADE,
                               blank=False,
                               related_name='portfolio')
    media_file = models.ForeignKey(MediaFile, on_delete=models.CASCADE)
