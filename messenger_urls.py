import os
CI_RUN = int(os.environ.get('CI_RUN', 0))

MESSENGER_HOST = 'localhost' if CI_RUN else '192.168.50.100'
MESSENGER_PORT = 5001 if CI_RUN else 5000
MESSENGER_URL = f'https://{MESSENGER_HOST}:{MESSENGER_PORT}'
HEALTH = '/health'
API = '/api'
LOGIN = API + '/login/'
LOGOUT = API + '/logout/'
USERS = API + '/users/'
MESSAGES = API + '/messages/'
