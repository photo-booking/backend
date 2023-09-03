# Generated by Django 4.2.4 on 2023-09-03 12:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MediaFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField(verbose_name='Ссылка на медиа файл')),
                ('title', models.CharField(max_length=25, verbose_name='Название')),
                ('media_type', models.CharField(max_length=25, verbose_name='Тип медиа файла')),
                ('is_main_photo', models.BooleanField(verbose_name='Отображение файла на главной')),
            ],
            options={
                'verbose_name': 'Медиа файл',
                'verbose_name_plural': 'Медиа файлы',
            },
        ),
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='portfolio', to=settings.AUTH_USER_MODEL)),
                ('media_file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.mediafile')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_service', models.CharField(max_length=25, verbose_name='Название услуги')),
                ('image_service', models.ImageField(blank=True, upload_to='users/tags', verbose_name='Фотография услуги')),
                ('cost_service', models.PositiveIntegerField(verbose_name='Стоимость услуги')),
                ('description_service', models.TextField(max_length=25, verbose_name='Описание услуги')),
                ('due_date', models.DateTimeField(verbose_name='Срок выполнения')),
                ('equipment', models.CharField(max_length=25, verbose_name='Оборудование')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'Услуга',
                'verbose_name_plural': 'Услуги',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=25, unique=True, verbose_name='имя')),
                ('slug', models.SlugField(unique=True, verbose_name='Индификатор')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ServiceMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('portfolio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service', to='services.portfolio')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='portfolio', to='services.service')),
            ],
        ),
        migrations.AddField(
            model_name='service',
            name='tag',
            field=models.ManyToManyField(blank=True, related_name='services', to='services.tag', verbose_name='Вид съемки'),
        ),
    ]
