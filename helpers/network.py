import os
import socket
import requests
from random import randint
from logger.logger import Logger


CI_RUN = int(os.environ.get('CI_RUN', 0))
current_dir = os.path.dirname(__file__)
repo_dir = os.path.abspath(os.path.join(current_dir, '..'))
cert_dir = 'cert-ci' if CI_RUN else 'cert'
SELF_SIGNED_CERT = os.path.join(repo_dir, cert_dir, 'certificate.pem')
network_logger = Logger('network_logger')


def find_free_port():
    port = randint(5005, 6000)
    counter = 0

    while counter <= 100:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

            if s.connect_ex(('localhost', port)) == 0:
                counter += 1
                continue
            else:
                return port

    return 0


def get_request(url, headers, params=None):
    try:
        response = requests.get(url, params=params, headers=headers, verify=SELF_SIGNED_CERT)
        network_logger.debug(f'Get response with:\n'
                             f'status code: {response.status_code}\n'
                             f'content: {response.content.decode()}')

        return response
    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout) as e:
        network_logger.error(e)
        return e


def post_request(url, headers, json_dict=None):
    try:
        response = requests.post(url, json=json_dict, headers=headers, verify=SELF_SIGNED_CERT)
        network_logger.debug(f'Post response with:\n'
                             f'status code: {response.status_code}\n'
                             f'content: {response.content.decode()}')
        return response
    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout) as e:
        network_logger.error(e)
        return e


def put_request(url, headers, json_dict=None):
    try:
        response = requests.put(url, json=json_dict, headers=headers, verify=SELF_SIGNED_CERT)
        network_logger.debug(f'Put response with:\n'
                             f'status code: {response.status_code}\n'
                             f'content: {response.content.decode()}')
        return response
    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout) as e:
        network_logger.error(e)
        return e


def patch_request(url, headers, json_dict=None):
    try:
        response = requests.patch(url, json=json_dict, headers=headers, verify=SELF_SIGNED_CERT)
        network_logger.debug(f'Patch response with:\n'
                             f'status code: {response.status_code}\n'
                             f'content: {response.content.decode()}')
        return response
    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout) as e:
        network_logger.error(e)
        return e


def delete_request(url, headers, json_dict=None):
    try:
        response = requests.delete(url, json=json_dict, headers=headers, verify=SELF_SIGNED_CERT)
        network_logger.debug(f'Delete response with:\n'
                             f'status code: {response.status_code}\n'
                             f'content: {response.content.decode()}')
        return response
    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout) as e:
        network_logger.error(e)
        return e


def get_local_ip():
    return socket.gethostbyname(socket.gethostname())
