from mock import patch
from rest_framework.test import APITestCase, APIClient
from ...models.user_article import UserArticle

from ...serializers.suscription_feed_serializer import SubscriptionFeedHelper
from ...auxiliary.helpers.test_helper import TestUtils
from http import HTTPStatus


class UserArticleReadStateTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.rss_url = "https://urlfalsadelfeedparser.com"
        cls.test_helper = TestUtils()

    @patch.object(SubscriptionFeedHelper, 'parse_data')
    def test_user_article_state_start_being_false(self, url_parser):

        url_parser.return_value = self.test_helper.false_subscription
        subscription_id = self.test_helper.submit_post_creating_user('newuser', {"link": self.rss_url}, self.client).data['id']
        resp = self.client.get('/main_app/subscriptions/' + str(subscription_id) +'/articles/').data
        self.assertEqual(resp[0]['read'] , False)

    @patch.object(SubscriptionFeedHelper, 'parse_data')
    def test_user_article_read_state_can_be_changed_to_true(self, url_parser):
        url_parser.return_value = self.test_helper.false_subscription
        subscription_id = self.test_helper.submit_post_creating_user('newuser', {"link": self.rss_url}, self.client).data['id']
        user_article_pk= self.client.get('/main_app/subscriptions/' + str(subscription_id) + '/articles/').data[0]['pk']
        data = {"read": True}
        resp = self.client.put('/main_app/articles/' + str(user_article_pk) + '/',data, format="json")
        user_article = UserArticle.objects.first()
        self.assertEqual(resp.status_code, HTTPStatus.OK)
        self.assertEqual(user_article.read, True)

    @patch.object(SubscriptionFeedHelper, 'parse_data')
    def test_user_article_state_can_be_changed_to_false_after_being_true(self,url_parser):
        url_parser.return_value = self.test_helper.false_subscription
        subscription_id = self.test_helper.submit_post_creating_user('newuser', {"link": self.rss_url}, self.client).data['id']
        user_article_pk = self.client.get('/main_app/subscriptions/' + str(subscription_id) + '/articles/').data[0]['pk']
        data_true = {"read": True}
        data_false = {"read": False}
        resp = self.client.put('/main_app/articles/' + str(user_article_pk) + '/', data_true,format="json")
        user_article = UserArticle.objects.first()
        self.assertEqual(user_article.read, True)
        resp = self.client.put('/main_app/articles/' + str(user_article_pk) + '/', data_false,format="json")
        user_article = UserArticle.objects.first()
        self.assertEqual(user_article.read, False)

    @patch.object(SubscriptionFeedHelper, 'parse_data')
    def test_user_article_state_cannot_be_change_by_other_user(self,url_parser):
        url_parser.return_value = self.test_helper.false_subscription
        self.test_helper.submit_post_creating_user('newuser', {"link": self.rss_url}, self.client).data['id']
        self.test_helper.create_and_login_user('newuser2', self.client)

        user_article = UserArticle.objects.first()
        self.assertEqual(user_article.read, False)
        data= {"read": True}
        resp =self.client.put('/main_app/articles/' + str(user_article.pk) + '/',data,format="json")
        self.assertEqual(resp.status_code,HTTPStatus.BAD_REQUEST)
        self.assertEqual(resp.data['detail'],'This article does not exist or is not part of any of your subscriptions')
        self.assertEqual(user_article.read, False)






