# Generated by Django 4.2.4 on 2023-08-31 08:31

from django.db import migrations, models
import phone_field.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('services', '0001_initial'),
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
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(max_length=25, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=25, verbose_name='Фамилия')),
                ('profile_photo', models.ImageField(blank=True, upload_to='users/profile', verbose_name='Фото профиля')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Почта для регистрации')),
                ('contact_email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Почта для связи')),
                ('phone', phone_field.models.PhoneField(help_text='Телефон для контакта', max_length=31, verbose_name='Номер телефона')),
                ('work_experience', models.FloatField(default=0, verbose_name='Опыт работы')),
                ('city', models.CharField(help_text='Укажите город проживания', max_length=25, verbose_name='Город')),
                ('raiting', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Рейтинг профиля')),
                ('about_me', models.TextField(max_length=500, verbose_name='Обо мне')),
                ('is_client', models.BooleanField(default=True, verbose_name='Роль.Клиент')),
                ('is_photographer', models.BooleanField(default=False, verbose_name='Роль.Фотограф')),
                ('is_video_operator', models.BooleanField(default=False, verbose_name='Роль.Видео-оператор')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='День рождения')),
                ('social_telegram', models.URLField(blank=True, null=True, verbose_name='Телеграм')),
                ('social_vkontakte', models.URLField(blank=True, null=True, verbose_name='Вконтакте')),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
                'ordering': ('email',),
            },
        ),
    ]
