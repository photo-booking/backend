import re
from django.core.exceptions import ValidationError


class MinMaxLengthValidator:
    def __init__(self, min_length=8, max_length=150):
        self.min_length = min_length
        self.max_length = max_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                'Этот пароль короткий, минимальная длина '
                f'{self.min_length} символов',
                code='invalid',
            )
        elif len(password) > self.max_length:
            raise ValidationError(
                'Этот пароль длинный, максимальная длина '
                f'{self.max_length} символов',
                code='invalid',
            )


class StructurePasswordValidator:
    def validate(self, message, user=None):
        incorrect_symbol = []
        for i in str(message):
            match = re.search(r'[@!#$%*+/=?^`{}‘|~\w+]', i, re.ASCII)
            if match is None:
                incorrect_symbol.append(i)
        if incorrect_symbol != []:
            raise ValidationError(
                'Проверьте корректность ввода пароля, '
                'есть символы которые нельзя использовать.'
                f'Неподходящие символы: {incorrect_symbol}',
                code='invalid',
            )


class NumericPasswordValidator:
    def validate(self, password, user=None):
        if password.isdigit():
            raise ValidationError(
                'Пароль состоит только из цифр',
                code="invalid",
            )
