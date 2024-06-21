import os
import sys
from locust import HttpUser, task, constant

# Fix for run via cmd inside venv
current_file = os.path.realpath(__file__)
current_dir = os.path.dirname(current_file)
repo_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.insert(0, repo_dir)

import messenger_urls
import messenger_test_data as test_data
from helpers.data import create_username, create_password, create_phone_number


SELF_SIGNED_CERT = os.path.abspath('../../cert/certificate.pem')


class TestLoad(HttpUser):

    def on_start(self):
        self.client.verify = SELF_SIGNED_CERT

    @task
    def check_health(self):
        self.client.head(messenger_urls.HEALTH)

    @task
    def check_login(self):
        self.client.post(messenger_urls.LOGIN, json={'username': test_data.USERNAME, 'password': test_data.PASSWORD,
                                                     'user_address': 'some_ip'})

    @task
    def check_get_user(self):
        self.client.get(messenger_urls.USERS, params={'username': test_data.ANOTHER_USERNAME})

    @task
    def check_create_user(self):
        self.client.post(messenger_urls.USERS, json={'username': create_username(),
                                                     'phone_number': create_phone_number(),
                                                     'password': create_password(default=True)})
