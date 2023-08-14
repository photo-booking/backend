import re
from string import punctuation, whitespace

from django.conf import settings
from rest_framework.validators import ValidationError


def regex_test(value):
    """Проверяет на соотвествие введенных данных и возвращает True\False"""
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
            raise ValidationError(
                f'{self.message_user}{output_incorrect_symbols(value)}'
            )
        return value.lower()


class CorrectEmail:
    """Проверка email на корректность."""
    message_email = (
        'Некоректный email, проверьте корректность написания'
    )

    def __init__(self, email):
        self.email = email

    def is_email_valid(self, email):
        valid_chars = {'-', '_', '.'}
        invalid_chars = set(punctuation + whitespace) - valid_chars
        stripped_email = email.strip()

        if "@" not in stripped_email:
            return False

        if stripped_email.count("@") != 1:
            return False

        local, domain = stripped_email.split("@")

        for char in invalid_chars:
            if (
                char in local
                and (not local.startswith('"')
                    or not local.endswith('"'))):
                return False

        if "." in local:
            try:
                dot_position_in_local = local.index(".")

                if local[dot_position_in_local + 1] == ".":
                    return False
            except:
                return False

        if local.startswith(".") or local.endswith("."):
            return False

        if domain.startswith("-") or domain.endswith("-"):
            return False

        if domain.startswith(".") or domain.endswith("."):
            return False

        dot_position_in_domain = domain.index(".")

        if "." in domain and (
            domain[
                dot_position_in_domain
            ] == domain[
                dot_position_in_domain + 1
            ]
        ):
            return False

        return True

    def validate_email(self, value):
        if self.is_email_valid(value):
            return value.lower()
        else:
            raise ValidationError(
                f'{self.message_email}'
            )
