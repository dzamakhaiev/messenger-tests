import unittest
from time import sleep
from datetime import datetime

import messenger_test_data
from test_framework import TestFramework
from helpers.network import find_free_port
from helpers.data import generate_pem_keys, serialize_keys, deserialize_keys, encrypt_message, decrypt_message


class EncryptedMessagesTest(TestFramework):

    def setUp(self):
        private_key, public_key = generate_pem_keys()
        private_key_str, public_key_str = serialize_keys(private_key, public_key)

        self.user = self.create_new_user()
        self.user.private_key = private_key_str
        self.user.public_key = public_key_str

        # Log in as default user to send serialized public key to server
        self.log_in_with_listener_url(user=self.user, listener_port=find_free_port())
        self.msg_json = {'message': None, 'sender_id': self.user.user_id, 'sender_username': self.user.username,
                         'receiver_id': None, 'send_date': datetime.now().strftime(messenger_test_data.DATETIME_FORMAT)}

    def test_send_encrypted_message(self):
        # Create new user and keys for new user
        new_user_private_key, new_user_public_key = generate_pem_keys()
        private_key_str, public_key_str = serialize_keys(new_user_private_key, new_user_public_key)

        new_user = self.create_new_user()
        new_user.private_key = private_key_str
        new_user.public_key = public_key_str

        # Log in as new user to send serialized public key to server
        port = find_free_port()
        new_queue = self.run_client_listener(port)
        self.log_in_with_listener_url(new_user, port)

        # Get new user from server to receive user_id and public_key after new user logged in
        response = self.get_user({'username': new_user.username}, token=self.user.token)
        self.assertEqual(200, response.status_code, msg=response.text)
        new_user_public_key_str = response.json()['public_key']
        self.assertEqual(new_user_public_key_str, new_user.public_key)

        # Deserialize other user's public key and encrypt message (imitate sender side)
        new_user_public_key = deserialize_keys(public_pem=new_user_public_key_str)
        message = 'Test message encryption.'
        encrypted_message = encrypt_message(new_user_public_key, message.encode('utf-8'))

        # Send encrypted message to new user
        msg_json = self.create_new_msg_json(receiver_id=new_user.user_id, message=encrypted_message)
        response = self.send_message(msg_json, token=self.user.token)

        # Check that message received
        self.assertEqual(200, response.status_code, msg=response.text)
        self.assertEqual(response.text, 'Message processed.')
        sleep(1)
        self.assertEqual(new_queue.qsize(), 1, 'No message in queue.')

        # Decrypt received message
        response_json = new_queue.get()
        received_message = response_json['message']
        received_message = bytes.fromhex(received_message)
        received_message = decrypt_message(new_user_private_key, received_message)
        self.assertEqual(message, received_message)


if __name__ == '__main__':
    unittest.main()
