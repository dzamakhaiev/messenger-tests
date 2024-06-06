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


def create_user(default_pwd=False):
    username = create_username()
    phone_number = create_phone_number()
    password = create_password(default=default_pwd)
    return {'username': username,
            'phone_number': phone_number,
            'password': password}
