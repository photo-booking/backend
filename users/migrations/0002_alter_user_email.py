# Generated by Django 4.2.4 on 2023-09-11 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(
                error_messages={
                    "unique": "Пользователь с такой почтой уже зарегистрирован"
                },
                max_length=254,
                unique=True,
                verbose_name="Почта для регистрации",
            ),
        ),
    ]
