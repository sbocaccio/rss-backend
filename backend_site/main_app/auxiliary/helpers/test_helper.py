from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase, APIClient


class TestUtils(TestCase):

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
    false_subscription_with_10_other_articles = {'link': 'https://falseurl.com', 'title': "Mom",
                                           'entries': [{'title': 'Title11', 'link': 'false_link11',
                                                        'summary': 'false_summary11'},
                                                       {'title': 'Title12', 'link': 'false_link12',
                                                        'summary': 'false_summary12'},
                                                       {'title': 'Title13', 'link': 'false_link13',
                                                        'summary': 'false_summary13'},
                                                       {'title': 'Title14', 'link': 'false_link14',
                                                        'summary': 'false_summary14'},
                                                       {'title': 'Title15', 'link': 'false_link15',
                                                        'summary': 'false_summary15'},
                                                       {'title': 'Title16', 'link': 'false_link16',
                                                        'summary': 'false_summary16'},
                                                       {'title': 'Title17', 'link': 'false_link17',
                                                        'summary': 'false_summary17'},
                                                       {'title': 'Title18', 'link': 'false_link18',
                                                        'summary': 'false_summary18'},
                                                       {'title': 'Title19', 'link': 'false_link19',
                                                        'summary': 'false_summary19'},
                                                       {'title': 'Title20', 'link': 'false_link20',
                                                        'summary': 'false_summary20'},
                                                       ]}

    def create_and_login_user(self, username, client):
        data = {"username": username, "password": 'password123', "email": 'newuser@gmail.com'}
        resp = client.post('/main_app/register/', data).json()
        token = resp['access']

        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def submit_post_creating_user(self, username, data,client):
        self.create_and_login_user(username, client)
        resp = client.post("/main_app/feed/", data)
        return resp


