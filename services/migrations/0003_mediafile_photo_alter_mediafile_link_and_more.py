# Generated by Django 4.2.4 on 2023-09-10 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="mediafile",
            name="photo",
            field=models.ImageField(
                blank=True, upload_to="users/photos", verbose_name="Фотография"
            ),
        ),
        migrations.AlterField(
            model_name="mediafile",
            name="link",
            field=models.URLField(blank=True, verbose_name="Ссылка на видео"),
        ),
        migrations.AlterField(
            model_name="mediafile",
            name="media_type",
            field=models.CharField(
                choices=[("VIDEO", "Video"), ("PHOTO", "Photo")],
                verbose_name="Тип медиа файла",
            ),
        ),
        migrations.AddConstraint(
            model_name="mediafile",
            constraint=models.CheckConstraint(
                check=models.Q(
                    ("photo__exact", ""), ("link__exact", ""), _connector="OR"
                ),
                name="Укажите только один вид медиа",
            ),
        ),
    ]