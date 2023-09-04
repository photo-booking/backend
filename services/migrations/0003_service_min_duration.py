# Generated by Django 4.2.4 on 2023-09-04 20:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_remove_service_author_service_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='min_duration',
            field=models.PositiveSmallIntegerField(default=1, help_text='введите время съемки в часах', validators=[django.core.validators.MinValueValidator(1, 'минимальное значение 1')], verbose_name='Минимальное время съемки в часах'),
            preserve_default=False,
        ),
    ]
