from django.conf import settings
from django.db import models

from services.models import Service
from users.models import User


class Chat(models.Model):
    name = models.CharField(
        verbose_name='Название чата',
        max_length=settings.MAX_LEN_NAME
    )
    users = models.ManyToManyField(
        User,
        verbose_name='Участники чата',
        related_name='chats'
    )

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'

    def __str__(self):
        return self.name


class Order(models.Model):
    name = models.CharField(
        verbose_name='Название заказа',
        max_length=settings.MAX_LEN_NAME
    )
    cost = models.PositiveIntegerField(
        verbose_name='Стоимость заказа',
    )
    date = models.DateField(
        verbose_name='Дата заказа',
        auto_now_add=True
    )
    completion_date = models.DateTimeField(
        verbose_name='Время исполнения'
    )
    status = models.BooleanField(
        verbose_name='Статус выполнения заказа',
        default=False
    )
    users = models.ManyToManyField(
        User,
        verbose_name='Участники сделки',
        related_name='orders'
    )
    service = models.ForeignKey(
        Service,
        verbose_name='Услуга в заказе',
        related_name='orders',
        on_delete=models.CASCADE
    )
    chat = models.ForeignKey(
        Chat,
        verbose_name='Чат',
        related_name='orders',
        on_delete=models.CASCADE
    )
    REQUIRED_FIELDS = (
        'name',
        'cost',
        'completion_date',
        'phone',
        'city'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return self.name


class Message(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name='Участник чата',
        related_name='messages',
        on_delete=models.CASCADE
    )
    text = models.TextField(
        verbose_name='Текст сообщения'
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )

    class Meta:
        ordering = ('author',)
        verbose_name = 'Сообзение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return self.text


class Raiting(models.Model):
    order = models.ForeignKey(
        Order,
        verbose_name='',
        related_name='raitings',
        on_delete=models.CASCADE
    )
    user = models.ManyToManyField(
        User,
        verbose_name='Участники рейтинга',
        related_name='raitings'
    )
    raiting = models.PositiveSmallIntegerField(
        verbose_name='Оценка исполнителя',
        blank=True,
        null=True
    )

    class Meta:
        ordering = ('order',)
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'

    def __str__(self):
        return self.raiting
