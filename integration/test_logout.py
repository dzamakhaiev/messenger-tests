import unittest
from test_framework import TestFramework


class LogoutTest(TestFramework):

    def setUp(self):
        self.user = self.create_new_user()
        self.correct_json = {'username': self.user.username, 'password': self.user.password,
                             'user_address': 'some_ip', 'public_key': 'some_key'}

    def test_logout_positive(self):
        response = self.log_in(self.correct_json)
        self.assertEqual(response.status_code, 200, response.text)

        user_id = response.json().get('user_id')
        self.assertEqual(self.user.user_id, user_id, f'Incorrect user_id: {user_id}')
        token = response.json().get('token')
        self.assertIsInstance(token, str, f'Unexpected token data type: {token}')

        response = self.log_out(json_dict={'username': self.user.username}, token=token)
        self.assertEqual(200, response.status_code, msg=response.text)

    def test_logout_negative(self):
        response = self.log_in(self.correct_json)
        self.assertEqual(response.status_code, 200, response.text)

        response = self.log_out(json_dict={'username': self.user.username})
        self.assertEqual(401, response.status_code, msg=response.text)

    def test_incorrect_logout(self):
        response = self.log_in(self.correct_json)
        self.assertEqual(response.status_code, 200, response.text)
        token = response.json().get('token')

        response = self.log_out(json_dict={}, token=token)
        self.assertEqual(400, response.status_code, msg=response.text)
        self.assertEqual('Validation error.', response.text)

    def test_validation_error(self):
        response = self.log_in(self.correct_json)
        self.assertEqual(response.status_code, 200, response.text)
        token = response.json().get('token')

        response = self.log_out(json_dict={'username': 'some user'}, token=token)
        self.assertEqual(400, response.status_code, msg=response.text)
        self.assertEqual('Validation error.', response.text)


if __name__ == '__main__':
    unittest.main()
