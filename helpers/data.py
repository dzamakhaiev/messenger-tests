import copy
import string
from random import randint
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding


def create_username():
    return 'user_{}'.format(randint(1, 9999999))


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


def corrupt_json_field(json_dict: dict, incorrect_field: str, value='incorrect'):
    incorrect_dict = copy.copy(json_dict)

    if 'and' not in incorrect_field:
        incorrect_dict[incorrect_field] = value

    else:
        fields = incorrect_field.split('and')
        fields = [field.strip() for field in fields]
        for field in fields:
            incorrect_dict[field] = value

    return incorrect_dict


def remove_json_field(json_dict: dict, remove_field: str):
    incorrect_dict = copy.copy(json_dict)

    if 'and' not in remove_field:
        incorrect_dict.pop(remove_field)

    else:
        fields = remove_field.split('and')
        fields = [field.strip() for field in fields]
        for field in fields:
            incorrect_dict.pop(field)

    return incorrect_dict


def generate_pem_keys():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    return private_key, public_key


def serialize_keys(private_key, public_key):
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption())

    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo)

    return private_pem.decode('utf-8'), public_pem.decode('utf-8')


def deserialize_keys(private_pem: str = None, public_pem: str = None):
    if private_pem:
        private_key = serialization.load_pem_private_key(private_pem.encode('utf-8'), password=None)
        return private_key

    if public_pem:
        public_key = serialization.load_pem_public_key(public_pem.encode('utf-8'))
        return public_key


def encrypt_message(public_key, message: bytes):
    encrypted_message = public_key.encrypt(
        message, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
    return encrypted_message.hex()


def decrypt_message(private_key, encrypted_message):
    decrypted_message = private_key.decrypt(
        encrypted_message,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
    return decrypted_message.decode('utf-8')
