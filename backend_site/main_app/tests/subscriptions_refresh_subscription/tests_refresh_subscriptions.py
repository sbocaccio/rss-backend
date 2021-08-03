from django.contrib.auth.models import User
from http import HTTPStatus
from mock import patch
from rest_framework.test import APITestCase

from ...auxiliary.helpers.test_helper import TestUtils
from ...models.article import Article
from ...models.subscription_feed_model import SubscriptionFeeds
from ...auxiliary.helpers.feed_helper import SubscriptionFeedHelper


class RefreshSubscriptionsTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.rss_url = "https://urlfalsadelfeedparser.com"
        cls.test_helper = TestUtils()

    @patch.object(SubscriptionFeedHelper, 'parse_data')
    def test_user_can_refresh_subscription(self, url_parser):
        url_parser.return_value = self.test_helper.false_subscription
        subscription = SubscriptionFeeds.objects.create(link='https://falseurl.com')
        self.test_helper.create_and_login_user('newuser', self.client)
        user = User.objects.get(id=1)
        subscription.users_subscribed.add(user)
        resp = self.client.put('/main_app/subscriptions/1/')
        self.assertEqual(resp.status_code, HTTPStatus.OK)

    def test_user_can_not_refresh_subscription_if_not_subscribed(self):
        SubscriptionFeeds.objects.create(link='https://falseurl.com')
        self.test_helper.create_and_login_user('newuser', self.client)
        resp = self.client.put('/main_app/subscriptions/1/')
        self.assertEqual(resp.data['detail'], 'You are not subscribed to that feed. Subscribe first.')

    @patch.object(SubscriptionFeedHelper, 'parse_data')
    def test_user_old_articles_are_not_deleted_when_max_limit_not_passed(self, url_parser):
        url_parser.return_value = self.test_helper.false_subscription
        resp = self.test_helper.submit_post_creating_user('newuser', {"link": self.rss_url}, self.client)
        self.assertEqual(len(Article.objects.all()), 1)
        url_parser.return_value = self.test_helper.false_subscription_with_other_articles
        resp = self.client.put('/main_app/subscriptions/1/').data
        self.assertEqual(len(Article.objects.all()), 2)

    @patch.object(SubscriptionFeedHelper, 'parse_data')
    def test_user_old_articles_are_deleted_when_max_limit_is_passed(self, url_parser):
        url_parser.return_value = self.test_helper.false_subscription
        resp = self.test_helper.submit_post_creating_user('newuser', {"link": self.rss_url}, self.client)
        self.assertEqual(len(Article.objects.all()), 1)
        url_parser.return_value = self.test_helper.false_subscription_with_10_articles
        resp = self.client.put('/main_app/subscriptions/1/').data
        self.assertEqual(len(Article.objects.all()), 10)


