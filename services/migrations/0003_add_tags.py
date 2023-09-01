from django.db import migrations

from services.tags_initializing import INITIAL_TAGS


def add_tags(apps, schema_editor):
    Tag = apps.get_model('services', 'Tag')
    for tag in INITIAL_TAGS:
        new_tag = Tag(name=tag['name'], slug=tag['slug'])
        new_tag.save()


def remove_tags(apps, schema_editor):
    Tag = apps.get_model('services', 'Tag')
    for tag in INITIAL_TAGS:
        Tag.objects.get(slug=tag['slug']).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('services', '0002_tag_service_author_service_tag')
    ]

    operations = [
        migrations.RunPython(add_tags, remove_tags)
    ]
