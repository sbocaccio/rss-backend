from django.contrib.auth.models import User
from http import HTTPStatus
from mock import patch
from rest_framework.test import APITestCase, APIClient

from ...auxiliary.helpers.test_helper import TestHelper
from ...models.article import Article
from ...models.subscription_feed_model import SubscriptionFeeds
from ...serializers.suscription_feed_serializer import FeedHelper


class DisplayArticlesTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.rss_url = "https://urlfalsadelfeedparser.com"
        cls.test_helper = TestHelper()

    def create_and_login_user(self, username):
        data = {"username": username, "password": 'password123', "email": 'newuser@gmail.com'}
        resp = self.client.post('/main_app/register/', data)
        token = resp.json().get('access')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def submit_post_creating_user(self, username, data):
        self.create_and_login_user(username)
        self.client.post("/main_app/feed/", data)

    @patch.object(FeedHelper, 'parse_data')
    def test_create_a_post_generates_an_article(self, url_parser):
        mock_value = {'link': 'https://falseurl.com', 'title': "Mom",
                      'entries': [{'title': 'Title', 'link': 'falselink', 'summary': 'false_summary'}]}
        url_parser.return_value = mock_value
        self.test_helper.submit_post_creating_user('newuser', {"link": self.rss_url}, self.client)
        self.assertEqual(len(Article.objects.all()), 1)

    @patch.object(FeedHelper, 'parse_data')
    def test_articles_have_one_user_and_correct_data_when_they_are_created(self, url_parser):
        mock_value = {'link': 'https://falseurl.com', 'title': "Mom",
                      'entries': [{'title': 'Title', 'link': 'false_link', 'summary': 'false_summary'}]}
        url_parser.return_value = mock_value
        self.test_helper.submit_post_creating_user('newuser', {"link": self.rss_url}, self.client)
        user1 = User.objects.filter(username='newuser')[0]
        articles = Article.objects.filter(users_subscribed=user1)
        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].title, 'Title')
        self.assertEqual(articles[0].link, 'false_link')
        self.assertEqual(articles[0].summary, 'false_summary')

    @patch.object(FeedHelper, 'parse_data')
    def test_articles_can_be_retrieved_passing_subscription_as_parameter(self, url_parser):
        mock_value = {'link': 'https://falseurl.com', 'title': "Mom",
                      'entries': [{'title': 'Title', 'link': 'false_link', 'summary': 'false_summary'}]}
        url_parser.return_value = mock_value
        self.test_helper.submit_post_creating_user('newuser', {"link": self.rss_url}, self.client)
        resp = self.client.get('/main_app/subscriptions/1/articles/')
        resp_articles = resp.json()
        self.assertEqual(resp.status_code, HTTPStatus.OK)
        self.assertEqual(len(resp_articles), 1)
        self.assertEqual(resp_articles[0]['title'], 'Title')
        self.assertEqual(resp_articles[0]['link'], 'false_link')
        self.assertEqual(resp_articles[0]['summary'], 'false_summary')


@patch.object(FeedHelper, 'parse_data')
def test_user_can_not_receive_articles_of_a_subscription_is_not_subscribed(self, url_parser):
    mock_value = {'link': 'https://falseurl.com', 'title': "Mom",
                  'entries': [{'title': 'Titulo', 'link': 'linkfalso', 'summary': 'summaryfalso'}]}
    url_parser.return_value = mock_value
    self.test_helper.submit_post_creating_user('newuser', {"link": self.rss_url}, self.client)
    resp = self.client.get('/main_app/subscriptions/2/articles/')
    self.assertEqual(resp.status_code, HTTPStatus.BAD_REQUEST)
    self.assertEqual(resp.json()['detail'], 'You are not subscribed to that feed. Subscribe first to read articles')
