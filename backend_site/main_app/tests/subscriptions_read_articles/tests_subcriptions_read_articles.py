from django.contrib.auth.models import User
from http import HTTPStatus
from mock import patch
from rest_framework.test import APITestCase, APIClient

from ...auxiliary.helpers.test_helper import TestUtils
from ...models.article import Article
from ...models.subscription_feed_model import SubscriptionFeeds
from ...models.user_article import UserArticle
from ...serializers.suscription_feed_serializer import SubscriptionFeedHelper



class DisplayArticlesTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.rss_url = "https://urlfalsadelfeedparser.com"
        cls.test_helper = TestUtils()

    @patch.object(SubscriptionFeedHelper, 'parse_data')
    def test_create_a_post_generates_an_article(self, url_parser):
        url_parser.return_value = self.test_helper.false_subscription
        self.test_helper.submit_post_creating_user('newuser', {"link": self.rss_url}, self.client)
        self.assertEqual(len(Article.objects.all()), 1)
        self.assertEqual(len(UserArticle.objects.all()), 1)

    @patch.object(SubscriptionFeedHelper, 'parse_data')
    def test_create_a_post_with_one_article_creates_two_user_articles_and_only_one_article(self, url_parser):
        url_parser.return_value = self.test_helper.false_subscription
        self.test_helper.submit_post_creating_user('newuser', {"link": self.rss_url}, self.client)
        self.test_helper.submit_post_creating_user('newuser2', {"link": self.rss_url}, self.client)
        self.assertEqual(len(Article.objects.all()), 1)
        self.assertEqual(len(UserArticle.objects.all()), 2)

    @patch.object(SubscriptionFeedHelper, 'parse_data')
    def test_user_article_and_article_have_correct_data_when_they_are_created(self, url_parser):
        url_parser.return_value = self.test_helper.false_subscription
        self.test_helper.submit_post_creating_user('newuser', {"link": self.rss_url}, self.client)
        user1 = User.objects.get(username='newuser')
        subscription_feed = SubscriptionFeeds.objects.get(id=1)
        user_article = UserArticle.objects.get(user=user1)
        article = user_article.article

        self.assertEqual(user_article.user, user1)
        self.assertEqual(user_article.read, False)


        self.assertEqual(article.title, 'Title')
        self.assertEqual(article.link, 'false_link')
        self.assertEqual(article.summary, 'false_summary')

    @patch.object(SubscriptionFeedHelper, 'parse_data')
    def test_articles_can_be_retrieved_passing_subscription_as_parameter(self, url_parser):
        url_parser.return_value = self.test_helper.false_subscription
        self.test_helper.submit_post_creating_user('newuser', {"link": self.rss_url}, self.client)
        resp = self.client.get('/main_app/subscriptions/1/articles/')
        resp_articles = resp.json()
        self.assertEqual(resp.status_code, HTTPStatus.OK)
        self.assertEqual(len(resp_articles), 1)
        self.assertEqual(resp_articles[0]['article']['title'], 'Title')
        self.assertEqual(resp_articles[0]['article']['link'], 'false_link')
        self.assertEqual(resp_articles[0]['article']['summary'], 'false_summary')

    @patch.object(SubscriptionFeedHelper, 'parse_data')
    def test_user_can_not_receive_articles_of_a_subscription_is_not_subscribed(self, url_parser):
        url_parser.return_value = self.test_helper.false_subscription
        self.test_helper.submit_post_creating_user('newuser', {"link": self.rss_url}, self.client)
        resp = self.client.get('/main_app/subscriptions/2/articles/')
        self.assertEqual(resp.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(resp.json()['detail'], 'You are not subscribed to that feed. Subscribe first.')

    @patch.object(SubscriptionFeedHelper, 'parse_data')
    def test_articles_are_received_in_inverse_date_time_when_there_are_many_articles(self, url_parser):
        mock_value = {'link': 'https://falseurl.com', 'title': "Mom",
                      'entries': [{'title': 'Title1', 'link': 'linkfalso', 'summary': 'false_summary2'},
                                  {'title': 'Title2', 'link': 'falselink2', 'summary': 'falsesummary2'}]}
        url_parser.return_value = mock_value
        self.test_helper.submit_post_creating_user('newuser', {"link": self.rss_url}, self.client)
        resp = self.client.get('/main_app/subscriptions/1/articles/')
        resp_articles = resp.json()
        self.assertEqual(resp_articles[0]['article']['title'], 'Title1')
        self.assertEqual(resp_articles[1]['article']['title'], 'Title2')


