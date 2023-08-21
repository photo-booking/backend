from django.conf import settings
from django.db import models


class PredefinedServiceType(models.Model):
    name = models.CharField(
        verbose_name='Название базовой услуги',
        max_length=settings.MAX_LEN_NAME,
        unique=True,
    )

    def __str__(self) -> str:
        return self.name


class CustomServiceType(PredefinedServiceType):
    worker = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='custom_service_types',
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        return self.name


class Service(models.Model):
    title = models.CharField(
        verbose_name='Название услуги', max_length=settings.MAX_LEN_NAME
    )
    service_image = models.ImageField(
        verbose_name='Фотография услуги',
        upload_to='users/images',
        blank=True,
    )
    price = models.PositiveIntegerField(verbose_name='Стоимость услуги')
    description = models.TextField(
        verbose_name='Описание услуги',
        max_length=settings.MAX_LEN_NAME,
        blank=True,
    )
    duration = models.PositiveIntegerField(
        verbose_name='Среднее время выполнения работы',
        help_text='указывается в минутах',
    )
    service_type = models.ForeignKey(
        PredefinedServiceType,
        on_delete=models.PROTECT,
        related_name='services',
    )
    worker = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='services'
    )

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    def __str__(self):
        return self.name
