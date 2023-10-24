from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from users.models import User


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviewer')
    service_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(validators=[
        MinValueValidator(limit_value=1,
                          message='Минимальное значение 1'),
        MaxValueValidator(limit_value=5,
                          message='Максимальное значение 5'),
        ])
    description = models.TextField('Текст отзыва', max_length=1000)
    post_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-post_date']

    def __str__(self):
        return f'{self.service_author} reviews'
