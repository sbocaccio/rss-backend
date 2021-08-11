from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase, APIClient


class TestUtils(TestCase):

    other_false_subscription = {'link': 'https://falseurl2.com', 'title': "Mom2",
                  'entries': [{'title': 'Title', 'link': 'false_link', 'summary': 'false_summary'}]}
    false_subscription = {'link': 'https://falseurl.com', 'title': "Mom",
                  'entries': [{'title': 'Title', 'link': 'false_link', 'summary': 'false_summary'}]}
    false_subscription_with_other_articles = {'link': 'https://falseurl.com', 'title': "Mom",
                  'entries': [{'title': 'Title2', 'link': 'false_link2', 'summary': 'false_summary2'}]}
    false_subscription_with_10_articles = {'link': 'https://falseurl.com', 'title': "Mom",
                  'entries': [{'title': 'Title01', 'link': 'false_link01', 'summary': 'false_summary01'},
                              {'title': 'Title02', 'link': 'false_link02', 'summary': 'false_summary02'},
                              {'title': 'Title03', 'link': 'false_link03', 'summary': 'false_summary03'},
                              {'title': 'Title04', 'link': 'false_link04', 'summary': 'false_summary04'},
                              {'title': 'Title05', 'link': 'false_link05', 'summary': 'false_summary05'},
                              {'title': 'Title06', 'link': 'false_link06', 'summary': 'false_summary06'},
                              {'title': 'Title07', 'link': 'false_link07', 'summary': 'false_summary07'},
                              {'title': 'Title08', 'link': 'false_link08', 'summary': 'false_summary08'},
                              {'title': 'Title09', 'link': 'false_link09', 'summary': 'false_summary09'},
                              {'title': 'Title10', 'link': 'false_link10', 'summary': 'false_summary10'},
                              ]}
    many_false_subscriptions= ['https://falseurl.com','https://falseurl2.com']
    def create_and_login_user(self, username, client):
        data = {"username": username, "password": 'password123', "email": 'newuser@gmail.com'}
        resp = client.post('/main_app/register/', data).json()
        token = resp['access']

        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def submit_post_creating_user(self, username, data,client):
        self.create_and_login_user(username, client)
        resp = client.post("/main_app/feed/", data)
        return resp


