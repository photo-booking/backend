# Generated by Django 4.2.4 on 2023-09-28 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0003_remove_service_equipment_service_order_delivery_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='due_date',
            field=models.DateTimeField(verbose_name='Начало выполнения'),
        ),
    ]