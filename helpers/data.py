import string
from random import randint


def create_username():
    return 'user_{}'.format(randint(1, 999999))


def create_phone_number():
    return '{}'.format(randint(10 ** 9, 10 ** 10 - 1))


def create_password(length=10, default=False):
    if default:
        return 'qwerty'

    password = ''
    for _ in range(length//2):
        password += string.ascii_letters
        password += str(randint(0, 9))

    return password
