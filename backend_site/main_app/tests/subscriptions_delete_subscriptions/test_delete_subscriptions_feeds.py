from mock import patch
from rest_framework.test import APITestCase, APIClient

from ...auxiliary.helpers.test_helper import TestUtils
from ...models.subscription_feed_model import SubscriptionFeeds
from ...models.user_article import UserArticle
from ...models.article import Article

from ...serializers.suscription_feed_serializer import SubscriptionFeedHelper


class DeleteSubscriptionsTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.rss_url = "https://urlfalsadelfeedparser.com"
        cls.test_helper = TestUtils()

    @patch.object(SubscriptionFeedHelper, 'parse_data')
    def test_user_can_delete_a_subscription(self, url_parser):
        mock_value = {'link': 'https://falseurl.com', 'title': "Mom",
                      'entries': [{'title': 'Title', 'link': 'falselink', 'summary': 'false_summary'}]}
        url_parser.return_value = mock_value
        self.test_helper.submit_post_creating_user('newuser', {"link": self.rss_url}, self.client)
        self.assertEqual(len(SubscriptionFeeds.objects.all()), 1)
        data = {'subscription_id': '1'}
        resp = self.client.delete('/main_app/feed/', data)
        self.assertEqual(resp.data['message'], 'Subscription Deleted correctly')
        self.assertEqual(len(SubscriptionFeeds.objects.all()), 0)

    @patch.object(SubscriptionFeedHelper, 'parse_data')
    def test_user_article_is_deleted_when_user_delete_its_subscription(self, url_parser):
        mock_value = {'link': 'https://falseurl.com', 'title': "Mom",
                      'entries': [{'title': 'Title', 'link': 'falselink', 'summary': 'false_summary'}]}
        url_parser.return_value = mock_value
        self.test_helper.submit_post_creating_user('newuser', {"link": self.rss_url}, self.client)
        self.assertEqual(len(UserArticle.objects.all()), 1)
        data = {'subscription_id': '1'}
        self.client.delete('/main_app/feed/', data)
        self.assertEqual(len(UserArticle.objects.all()), 0)



    @patch.object(SubscriptionFeedHelper, 'parse_data')
    def test_subscription_object_is_not_deleted_when_there_are_other_readers(self, url_parser):
        mock_value = {'link': 'https://falseurl.com', 'title': "Mom",
                      'entries': [{'title': 'Title', 'link': 'falselink', 'summary': 'false_summary'}]}
        url_parser.return_value = mock_value
        self.test_helper.submit_post_creating_user('newuser', {"link": self.rss_url}, self.client)
        self.test_helper.submit_post_creating_user('newuser2', {"link": self.rss_url}, self.client)
        self.assertEqual(len(SubscriptionFeeds.objects.all()), 1)
        data = {'subscription_id': '1'}
        self.client.delete('/main_app/feed/', data)
        self.assertEqual(len(SubscriptionFeeds.objects.all()), 1)

    @patch.object(SubscriptionFeedHelper, 'parse_data')
    def test_user_cannot_deleted_a_subscription_is_not_subscribe(self, url_parser):
        mock_value = {'link': 'https://falseurl.com', 'title': "Mom",
                      'entries': [{'title': 'Title', 'link': 'falselink', 'summary': 'false_summary'}]}
        url_parser.return_value = mock_value
        self.test_helper.submit_post_creating_user('newuser', {"link": self.rss_url}, self.client)
        mock_value = {'link': 'https://falseurl2.com', 'title': "Mom",
                      'entries': [{'title': 'Title', 'link': 'falselink', 'summary': 'false_summary'}]}
        url_parser.return_value = mock_value

        self.test_helper.submit_post_creating_user('newuser2', {"link": self.rss_url}, self.client)
        self.assertEqual(len(SubscriptionFeeds.objects.all()), 2)
        data = {'subscription_id': '1'}
        resp = self.client.delete('/main_app/feed/', data)
        self.assertEqual(resp.data['detail'], 'You are not subscribed to that feed. Subscribe first.')
        self.assertEqual(len(UserArticle.objects.all()), 2)


    @patch.object(SubscriptionFeedHelper, 'parse_data')
    def test_article_is_deleted_when_there_are_not_readers(self, url_parser):
        mock_value = {'link': 'https://falseurl.com', 'title': "Mom",
                      'entries': [{'title': 'Title', 'link': 'falselink', 'summary': 'false_summary'}]}
        url_parser.return_value = mock_value
        self.test_helper.submit_post_creating_user('newuser', {"link": self.rss_url}, self.client)
        self.assertEqual(len(Article.objects.all()), 1)
        data = {'subscription_id': '1'}
        self.client.delete('/main_app/feed/', data)
        self.assertEqual(len(Article.objects.all()), 0)

    @patch.object(SubscriptionFeedHelper, 'parse_data')
    def test_article_is_not_deleted_when_there_are_other_readers(self, url_parser):
        mock_value = {'link': 'https://falseurl.com', 'title': "Mom",
                      'entries': [{'title': 'Title', 'link': 'falselink', 'summary': 'false_summary'}]}
        url_parser.return_value = mock_value
        self.test_helper.submit_post_creating_user('newuser', {"link": self.rss_url}, self.client)
        self.test_helper.submit_post_creating_user('newuser2', {"link": self.rss_url}, self.client)
        self.assertEqual(len(Article.objects.all()), 1)
        data = {'subscription_id': '1'}
        self.client.delete('/main_app/feed/', data)
        self.assertEqual(len(Article.objects.all()), 1)

