# Generated by Django 4.2.4 on 2023-09-03 07:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FeedbackProperty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('raiting', models.PositiveSmallIntegerField(blank=True, verbose_name='Рейтинг предприятия')),
                ('descriptions', models.TextField(max_length=500, verbose_name='Текст обратной связи')),
            ],
            options={
                'verbose_name': 'Обратная связь',
                'verbose_name_plural': 'Обратные связи',
            },
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25, verbose_name='Название недвижимости')),
                ('adress', models.CharField(max_length=25, verbose_name='Адрес')),
                ('worktime', models.TextField(verbose_name='Время работы')),
                ('area', models.FloatField(verbose_name='Общая площадь помещений')),
                ('price', models.FloatField(verbose_name='Стоимость помещений')),
            ],
            options={
                'verbose_name': 'Недвижимость',
                'verbose_name_plural': 'Недвижимость',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25, verbose_name='Название помещния')),
                ('area', models.FloatField(verbose_name='Площадь помещения')),
                ('price', models.FloatField(verbose_name='Стоимость помещения')),
                ('property', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='properties.property', verbose_name='Номер комнаты')),
            ],
            options={
                'verbose_name': 'Комната в недвижимости',
                'verbose_name_plural': 'Комнаты в недвижимости',
            },
        ),
    ]
