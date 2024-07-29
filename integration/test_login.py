import unittest
from test_framework import TestFramework
from helpers.data import corrupt_json_field, remove_json_field


class LoginTest(TestFramework):

    def setUp(self):
        self.user = self.create_new_user()
        self.correct_json = {'username': self.user.username, 'password': self.user.password,
                             'user_address': 'some_ip', 'public_key': 'some_key'}

    def test_login_positive(self):
        response = self.log_in(self.correct_json)
        self.assertEqual(response.status_code, 200, response.text)

        user_id = response.json().get('user_id')
        self.assertEqual(self.user.user_id, user_id, f'Incorrect user_id: {user_id}')

        token = response.json().get('token')
        self.assertIsInstance(token, str, f'Unexpected token data type: {token}')

    def test_incorrect_login(self):
        for field in ('username', 'password', 'username and password'):

            with self.subTest(f'Login with incorrect "{field}" field.'):
                incorrect_json = corrupt_json_field(self.correct_json, field)
                response = self.log_in(incorrect_json)
                self.assertEqual(401, response.status_code, msg=response.text)
                self.assertEqual('Incorrect username or password.', response.text)

    def test_validation_error(self):
        for field in ('username', 'password', 'user_address', 'public_key'):

            with self.subTest(f'Login with no "{field}" field.'):
                incorrect_json = remove_json_field(self.correct_json, field)
                response = self.log_in(incorrect_json)
                self.assertEqual(400, response.status_code, msg=response.text)
                self.assertEqual('Validation error.', response.text)


if __name__ == '__main__':
    unittest.main()
