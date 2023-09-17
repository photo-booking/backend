import json
import os

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand

from services.models import Tag


class Command(BaseCommand):
    help = 'Импорт тэгов с json файла'

    def handle(self, *args, **options):
        tags = []
        try:
            with open(
                (os.path.join(settings.BASE_DIR, 'data/tags.json')),
                encoding='utf-8',
            ) as file_tags:
                data = json.load(file_tags)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('Файл не найден'))

        for tags in data:
            tags.append(Tag(name=tags['name'], slug=tags['slug']))
        try:
            Tag.objects.bulk_create(tags)
            self.stdout.write(self.style.SUCCESS("Тэги загружены"))
        except ValidationError as error:
            self.style.ERROR(
                'Ошибка загрузки файла с данными, ошибка {}'.format(str(error))
            )
