import json
import os
from pathlib import Path

INITIAL_TAGS = []


def fill_initial_data():
    data_folder = Path(__file__).resolve().parent.parent / 'data'
    file_path = os.path.join(
        data_folder, 'tags.json'
    )
    with open(file_path, encoding='utf-8') as tags:
        data = json.load(tags)
        for data_object in data:
            name = data_object.get('name', None)
            slug = data_object.get('slug', None)
            INITIAL_TAGS.append(
                {
                    'name': name,
                    'slug': slug
                }
            )


fill_initial_data()
