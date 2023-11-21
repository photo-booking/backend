from django.conf import settings
from django.db import models

from services.models import Service
from users.models import User


class Order(models.Model):
    name = models.CharField(
        verbose_name='Название заказа',
        max_length=settings.MAX_LEN_NAME
    )
    cost = models.PositiveIntegerField(
        verbose_name='Стоимость заказа',
    )
    date = models.DateField(verbose_name='Дата заказа', auto_now_add=True)
    completion_date = models.DateTimeField(verbose_name='Время исполнения')
    status = models.BooleanField(
        verbose_name='Статус выполнения заказа', default=False
    )
    customer_user = models.ForeignKey(
        User, verbose_name='Заказчик',
        related_name='customer_orders', on_delete=models.CASCADE,
    )
    executor_user = models.ForeignKey(
        User, verbose_name='Исполнитель заказа',
        related_name='executor_orders', on_delete=models.CASCADE,
    )
    service = models.ForeignKey(
        Service,
        verbose_name='Услуга в заказе',
        related_name='orders',
        on_delete=models.CASCADE,
    )
    REQUIRED_FIELDS = (
        'name', 'cost', 'date', 'customer_users',
        'executor_user', 'completion_date', 'service'
    )

    class Meta:
        ordering = ('date',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return self.name


class Raiting(models.Model):
    order = models.ForeignKey(
        Order,
        verbose_name='Название заказа',
        related_name='raitings',
        on_delete=models.CASCADE,
    )
    customer_user = models.ForeignKey(
        User, verbose_name='Заказчик',
        related_name='customer_raitings', on_delete=models.CASCADE,
    )
    executor_user = models.ForeignKey(
        User, verbose_name='Заказчик',
        related_name='executor_raitings', on_delete=models.CASCADE,
    )
    raiting = models.PositiveSmallIntegerField(
        verbose_name='Оценка исполнителя', blank=True, null=True
    )
    REQUIRED_FIELDS = (
        'order', 'customer_user',
        'executor_user', 'raiting'
    )

    class Meta:
        ordering = ('order',)
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'

    def __str__(self):
        return str(self.raiting)
