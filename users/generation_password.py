from random import choice
from string import ascii_uppercase, digits


def generation_password():
    uppercase = ''.join(choice(ascii_uppercase) for _ in range(20))
    digit = ''.join(choice(digits) for _ in range(20))
    return uppercase + digit
