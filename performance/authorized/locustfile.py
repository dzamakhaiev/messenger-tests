import os
import sys
import logging
from time import sleep
from random import uniform
from datetime import datetime
from locust import HttpUser, task, constant

# Fix for run via cmd inside venv
current_file = os.path.realpath(__file__)
current_dir = os.path.dirname(current_file)
repo_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.insert(0, repo_dir)

import messenger_urls
import messenger_test_data as test_data
from helpers.data import create_user


class TestLoad(HttpUser):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.msg_json = {'message': 'test', 'sender_id': None, 'sender_username': None,
                         'receiver_id': None, 'send_date': ''}
        self.headers = {'Content-type': 'application/json', 'Authorization': ''}

    def on_start(self):
        # Create new user to send messages
        logging.info('Create new user')
        sleep(uniform(0.25, 1.75))
        sender_user_json = create_user()
        response = self.client.post(messenger_urls.USERS, json=sender_user_json)
        logging.info(f'Response: {response.status_code} {response.text}')

        if response.status_code == 201:
            user_id = response.json().get('user_id')
            self.msg_json['sender_id'] = user_id
            self.msg_json['sender_username'] = sender_user_json.get('username')
        else:
            self.stop()

        # Create new user to receive messages
        user_json = create_user()
        response = self.client.post(messenger_urls.USERS, json=user_json)
        logging.info(f'Response: {response.status_code} {response.text}')

        if response.status_code == 201:
            receiver_id = response.json().get('user_id')
            self.msg_json['receiver_id'] = receiver_id
        else:
            self.stop()

        # Log in as sender
        response = self.client.post(messenger_urls.LOGIN, json={'username': sender_user_json.get('username'),
                                                                'password': sender_user_json.get('password'),
                                                                'user_address': 'some_ip'})
        logging.info(f'Response: {response.status_code} {response.text}')

        if response.status_code == 200:
            token = response.json().get('token')
            self.headers['Authorization'] = f'Bearer {token}'
        else:
            self.stop()

    @task
    def check_message(self):
        self.msg_json['send_date'] = datetime.now().strftime(test_data.DATETIME_FORMAT)
        self.client.post(messenger_urls.MESSAGES, json=self.msg_json, headers=self.headers)


