from django.conf import settings
from django.db import models

from users.models import User


class Property(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Владелец недвижимости',
        related_name='properties',
        on_delete=models.CASCADE,
        null=True,
    )
    name = models.CharField(
        verbose_name='Название недвижимости', max_length=settings.MAX_LEN_NAME
    )
    adress = models.CharField(
        verbose_name='Адрес', max_length=settings.MAX_LEN_NAME
    )
    worktime = models.TextField(verbose_name='Время работы')
    area = models.FloatField(verbose_name='Общая площадь помещений')
    price = models.FloatField(verbose_name='Стоимость помещений')

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
        null=True,
    )
    name = models.CharField(
        verbose_name='Название помещния', max_length=settings.MAX_LEN_NAME
    )
    area = models.FloatField(verbose_name='Площадь помещения')
    price = models.FloatField(verbose_name='Стоимость помещения')

    class Meta:
        verbose_name = 'Комната в недвижимости'
        verbose_name_plural = 'Комнаты в недвижимости'


class FeedbackProperty(models.Model):
    raiting = models.PositiveSmallIntegerField(
        verbose_name='Рейтинг предприятия', blank=True
    )
    descriptions = models.TextField(
        verbose_name='Текст обратной связи', max_length=settings.MAX_TEXT_LEN
    )
    user_client = models.ForeignKey(
        User,
        verbose_name='Клиент',
        related_name='feedback_properties',
        on_delete=models.CASCADE,
        null=True,
    )
    property = models.ForeignKey(
        Property,
        verbose_name='Название недвижимости',
        related_name='feedback_properties',
        on_delete=models.CASCADE,
        null=True,
    )

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратные связи'

    def __str__(self):
        return str(self.raiting)
