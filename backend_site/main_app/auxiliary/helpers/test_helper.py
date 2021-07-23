from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase, APIClient


class TestHelper(TestCase):

    def create_and_login_user(self, username, client):
        data = {"username": username, "password": 'password123', "email": 'newuser@gmail.com'}
        resp = client.post('/main_app/register/', data).json()
        token = resp['access']

        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def submit_post_creating_user(self, username, data,client):
        self.create_and_login_user(username, client)
        client.post("/main_app/feed/", data)
