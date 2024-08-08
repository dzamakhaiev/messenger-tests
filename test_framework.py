import unittest
import requests
from copy import copy
from time import sleep
from queue import Queue
from datetime import datetime

from helpers.data import create_username, create_phone_number, create_password
from helpers.listener import run_listener
from logger.logger import Logger
from helpers import network
import messenger_test_data
import messenger_urls

MESSENGER_URL = messenger_urls.MESSENGER_URL_CI
HEADERS = {'Content-type': 'application/json', 'Authorization': None}
framework_logger = Logger('framework_logger')


class User:

    def __init__(self, user_id, username, phone_number, password=messenger_test_data.PASSWORD):
        framework_logger.debug(f'Create user instance with attributes: '
                               f'{user_id, username, phone_number, password}')
        self.user_id = user_id
        self.username = username
        self.password = password
        self.phone_number = phone_number
        self.token = None
        self.user_address = None
        self.listener_port = None
        self.private_key = None
        self.public_key = None


class TestFramework(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        framework_logger.debug('Set up messenger URLs for TestFramework class. ')
        cls.login_url = MESSENGER_URL + messenger_urls.LOGIN
        cls.logout_url = MESSENGER_URL + messenger_urls.LOGOUT
        cls.users_url = MESSENGER_URL + messenger_urls.USERS
        cls.messages_url = MESSENGER_URL + messenger_urls.MESSAGES
        cls.users = []
        cls.msg_json = {}

    def request(self, url, json_dict, headers, sleep_time=0.1, request_type='post'):
        framework_logger.info(f'{request_type} request to URL: {url}\n'
                              f'json: {json_dict}\n'
                              f'headers: {headers}')

        if request_type == 'get':
            response = network.get_request(url, headers, json_dict)
        elif request_type == 'post':
            response = network.post_request(url, headers, json_dict)
        elif request_type == 'put':
            response = network.put_request(url, headers, json_dict)
        elif request_type == 'patch':
            response = network.patch_request(url, headers, json_dict)
        elif request_type == 'delete':
            response = network.delete_request(url, headers, json_dict)
        else:
            raise NotImplementedError

        if isinstance(response, requests.ConnectionError):
            self.fail(f'Request failed: {response}')
        sleep(sleep_time)
        return response

    def get_user(self, json_dict, token=None):
        headers = copy(HEADERS)
        if token:
            headers['Authorization'] = f'Bearer {token}'
        response = self.request(url=self.users_url, json_dict=json_dict, request_type='get', headers=headers)
        return response

    def create_user(self, json_dict):
        response = self.request(url=self.users_url, json_dict=json_dict, request_type='post', headers=HEADERS)
        return response

    def delete_user(self, json_dict):
        response = self.request(url=self.users_url, json_dict=json_dict, request_type='delete', headers=HEADERS)
        return response

    def send_message(self, json_dict, sleep_time=0.1, token=None):
        headers = copy(HEADERS)
        if token:
            headers['Authorization'] = f'Bearer {token}'

        response = self.request(url=self.messages_url, json_dict=json_dict, sleep_time=sleep_time, headers=headers)
        return response

    def log_in(self, json_dict):
        response = self.request(url=self.login_url, json_dict=json_dict, headers=HEADERS)
        return response

    def log_out(self, json_dict, token=None):
        headers = copy(HEADERS)
        if token:
            headers['Authorization'] = f'Bearer {token}'

        response = self.request(url=self.logout_url, json_dict=json_dict, headers=headers)
        return response

    def log_in_with_listener_url(self, user: User, listener_port):
        local_host_ip = network.get_local_ip()
        user.user_address = f'http://{local_host_ip}:{listener_port}'
        user.listener_port = listener_port
        user.public_key = user.public_key if user.public_key else 'some_key'

        login_json = {'username': user.username, 'password': user.password,
                      'user_address': user.user_address, 'public_key': user.public_key}
        response = self.log_in(login_json)

        if response.status_code == 200:
            user.token = response.json()['token']

        else:
            self.fail(response.text)
        return response

    def create_new_user(self):
        username = create_username()
        phone_number = create_phone_number()
        password = create_password(default=True)
        user_json = {'username': username, 'phone_number': phone_number, 'password': password, 'request': 'create_user'}

        response = self.create_user(user_json)
        if response.status_code == 201:
            user_id = response.json()['user_id']
            user = User(user_id=user_id, username=username, phone_number=phone_number)
            self.users.append(user)

        else:
            self.fail(response.text)

        return user

    def delete_new_user(self, user: User):
        user_json = {'user_id': user.user_id}
        response = self.delete_user(user_json)
        return response

    def create_new_msg_json(self, **kwargs):
        msg_json = copy(self.msg_json)
        msg_json['sender_id'] = kwargs.get('sender_id', msg_json['sender_id'])
        msg_json['sender_username'] = kwargs.get('sender_username', msg_json['sender_username'])
        msg_json['receiver_id'] = kwargs.get('receiver_id', msg_json['receiver_id'])
        msg_json['message'] = kwargs.get('message', msg_json['message'])
        msg_json['send_date'] = datetime.now().strftime(messenger_test_data.DATETIME_FORMAT)
        return msg_json

    @staticmethod
    def run_client_listener(port):
        queue = Queue()
        run_listener(queue, port=port)
        return queue

    def tearDown(self):
        if self.users:
            for user in self.users:
                self.delete_new_user(user)
