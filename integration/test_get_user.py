import unittest
from test_framework import TestFramework
from helpers.data import corrupt_json_field, remove_json_field


class GetUserTest(TestFramework):

    def setUp(self):
        self.user = self.create_new_user()
        self.user.public_key = 'some_key'
        response = self.log_in({'username': self.user.username, 'password': self.user.password,
                                'user_address': 'some_ip', 'public_key': self.user.public_key})
        self.user.token = response.json().get('token')
        self.correct_json = {'username': self.user.username}

    def test_get_user_id_positive(self):
        response = self.get_user(self.correct_json, token=self.user.token)
        self.assertEqual(200, response.status_code, msg=response.text)

        user_id = response.json()['user_id']
        self.assertEqual(self.user.user_id, user_id, f'Incorrect user_id: {user_id}')
        public_key = response.json()['public_key']
        self.assertEqual(self.user.public_key, public_key, f'Incorrect public_key: {public_key}')

    def test_validation_error(self):
        incorrect_json = remove_json_field(self.correct_json, 'username')
        response = self.get_user(incorrect_json, token=self.user.token)
        self.assertEqual(400, response.status_code, msg=response.text)

    def test_incorrect_data(self):
        incorrect_json = corrupt_json_field(self.correct_json, 'username')
        response = self.get_user(incorrect_json, token=self.user.token)
        self.assertEqual(404, response.status_code, msg=response.text)


if __name__ == '__main__':
    unittest.main()
