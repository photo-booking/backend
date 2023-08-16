import re

from django.conf import settings
from rest_framework import serializers


def regex_test(value):
    """Проверяет на соотвествие введенных данных и возвращает True/False"""
    return bool(re.match('^[a-zA-Z0-9.@+-_]+$', value))


def output_incorrect_symbols(value):
    """Возвращает список из некоректно веденных символов"""
    incorrect_symbols = []
    for letter in list(value):
        if not re.match('^[a-zA-Z0-9.@+-_]+$', letter):
            incorrect_symbols.append(letter)
    return incorrect_symbols


class CorrectUsernameAndNotMe:
    """Проверка username на корректность и несоответствие "me"."""
    message_user = (
        'Можно использовать латиницу, цифры, @+-_. Нельзя использовать:'
    )

    def __init__(self, value):
        self.value = value

    def validate_username(self, value):
        if (value == settings.NO_REGISTER_USERNAME
                or not regex_test(value)):
            raise serializers.ValidationError(
                f'{self.message_user}{output_incorrect_symbols(value)}'
            )
        return value.lower()
