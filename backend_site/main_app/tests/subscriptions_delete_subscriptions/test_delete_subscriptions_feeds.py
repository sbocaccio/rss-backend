from http import HTTPStatus
from mock import patch
from rest_framework.test import APITestCase, APIClient

from ...auxiliary.helpers.test_helper import TestUtils
from ...models.article import Article
from ...models.subscription_feed_model import SubscriptionFeeds
from ...models.user_article import UserArticle
from ...serializers.suscription_feed_serializer import SubscriptionFeedHelper
from django.contrib.auth.models import User


class DeleteSubscriptionsTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.rss_url = "https://urlfalsadelfeedparser.com"
        cls.test_helper = TestUtils()


    def test_user_can_delete_a_subscription(self):
        self.test_helper.create_and_login_user('newuser',self.client)
        user = User.objects.first()
        subscription = SubscriptionFeeds.objects.create(link='https://falseurl.com')
        subscription.users_subscribed.add(user)
        resp = self.client.delete('/main_app/subscriptions/1/')
        self.assertEqual(resp.status_code, HTTPStatus.NO_CONTENT)
        self.assertEqual(len(SubscriptionFeeds.objects.all()), 0)

    @patch.object(SubscriptionFeedHelper, 'parse_data')
    def test_user_article_is_deleted_when_user_delete_its_subscription(self, url_parser):
        url_parser.return_value = self.test_helper.false_subscription
        self.test_helper.submit_post_creating_user('newuser', {"link": self.rss_url}, self.client)
        resp = self.client.delete('/main_app/subscriptions/1/')
        self.assertEqual(len(UserArticle.objects.all()), 0)


    def test_subscription_object_is_not_deleted_when_there_are_other_readers(self):
        subscription = SubscriptionFeeds.objects.create(link='https://falseurl.com')
        self.test_helper.create_and_login_user('newuser',self.client)
        user1 = User.objects.create_user('username', password='password',     email='email@email.com')
        user2 = User.objects.get(id=2)
        subscription.users_subscribed.add(user1)
        subscription.users_subscribed.add(user2)
        self.assertEqual(len(SubscriptionFeeds.objects.all()), 1)
        self.client.delete('/main_app/subscriptions/1/')
        self.assertEqual(len(SubscriptionFeeds.objects.all()), 1)

    def test_user_cannot_deleted_a_subscription_is_not_subscribe(self):
        subscription = SubscriptionFeeds.objects.create(link='https://falseurl.com')
        other_user = User.objects.create_user('username', password='password', email='email@email.com')
        subscription.users_subscribed.add(other_user)
        self.test_helper.create_and_login_user('newuser', self.client)

        self.assertEqual(len(SubscriptionFeeds.objects.all()), 1)
        resp = self.client.delete('/main_app/subscriptions/1/')
        self.assertEqual(resp.data['detail'], 'You are not subscribed to that feed. Subscribe first.')
        self.assertEqual(len(SubscriptionFeeds.objects.all()), 1)

    def test_user_cannot_deleted_a_not_existent_subscription(self):
        self.test_helper.create_and_login_user('newuser',self.client)
        resp = self.client.delete('/main_app/subscriptions/1/')
        self.assertEqual(resp.data['detail'], 'You are not subscribed to that feed. Subscribe first.')
        self.assertEqual(len(SubscriptionFeeds.objects.all()), 0)

    @patch.object(SubscriptionFeedHelper, 'parse_data')
    def test_article_is_deleted_when_there_are_not_readers(self, url_parser):
        url_parser.return_value = self.test_helper.false_subscription_with_other_articles
        self.test_helper.submit_post_creating_user('newuser', {"link": self.rss_url}, self.client)

        subscription_id = SubscriptionFeeds.objects.get().id
        link  = '/main_app/subscriptions/' + str(subscription_id) + '/'
        self.assertEqual(len(Article.objects.all()), 1)
        resp = self.client.delete(link)
        self.assertEqual(len(SubscriptionFeeds.objects.all()), 0)
        self.assertEqual(len(UserArticle.objects.all()), 0)


    @patch.object(SubscriptionFeedHelper, 'parse_data')
    def test_article_is_not_deleted_when_there_are_other_readers(self, url_parser):
        url_parser.return_value = self.test_helper.false_subscription
        self.test_helper.submit_post_creating_user('newuser', {"link": self.rss_url}, self.client)
        self.test_helper.submit_post_creating_user('newuser2', {"link": self.rss_url}, self.client)
        self.assertEqual(len(Article.objects.all()), 1)
        self.client.delete('/main_app/subscriptions/1/')
        self.assertEqual(len(Article.objects.all()), 1)

    @patch.object(SubscriptionFeedHelper, 'parse_data')
    def test_user_article_is_not_deleted_if_article_belongs_to_many_subscriptions(self,url_parser):

        mock_value = {'link': 'https://falseurl.com', 'title': "Mom",
                      'entries': [{'title': 'Title', 'link': 'falselink', 'summary': 'false_summary'}]}
        url_parser.return_value = mock_value
        self.test_helper.submit_post_creating_user('newuser', {"link": self.rss_url}, self.client)
        mock_value = {'link': 'https://falseurl.com2', 'title': "Mom",
                      'entries': [{'title': 'Title', 'link': 'falselink', 'summary': 'false_summary'}]}
        url_parser.return_value = mock_value
        self.client.post("/main_app/feed/", {"link": self.rss_url})
        self.assertEqual(len(UserArticle.objects.all()), 1)
        self.client.delete('/main_app/subscriptions/1/')
        self.assertEqual(len(UserArticle.objects.all()), 1)

