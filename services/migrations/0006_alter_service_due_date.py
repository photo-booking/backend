# Generated by Django 4.2.4 on 2023-10-02 06:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0005_alter_service_due_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='due_date',
            field=models.DateTimeField(default=datetime.date(2023, 10, 2), verbose_name='Начало выполнения'),
        ),
    ]
