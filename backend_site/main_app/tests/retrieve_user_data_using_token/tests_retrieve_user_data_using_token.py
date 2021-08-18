from http import HTTPStatus
from rest_framework.test import APITestCase, APIClient

from ...auxiliary.helpers.test_helper import TestUtils


class ValidateTokenTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_helper = TestUtils()

    def test_correct_token_gets_username_when_validating_token(self):
        self.test_helper.create_and_login_user('usuario', self.client)
        resp = self.client.get('/user_data/')

        self.assertEqual(resp.status_code, HTTPStatus.OK)
        self.assertEqual(resp.data['username'], 'usuario')

    def test_invalid_token_gets_unauthorized(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + '123')
        resp = self.client.get('/user_data/')
        self.assertEqual(resp.status_code, HTTPStatus.UNAUTHORIZED)
