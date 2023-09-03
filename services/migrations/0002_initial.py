# Generated by Django 4.2.4 on 2023-09-01 08:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('services', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AddField(
            model_name='service',
            name='tag',
            field=models.ManyToManyField(blank=True, related_name='services', to='services.tag', verbose_name='Вид съемки'),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='media_file',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.mediafile'),
        ),
    ]