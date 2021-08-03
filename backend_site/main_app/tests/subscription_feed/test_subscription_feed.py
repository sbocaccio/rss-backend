from django.contrib.auth.models import User
from http import HTTPStatus
from mock import patch
from rest_framework.test import APITestCase, APIClient

from ...auxiliary.helpers.test_helper import TestUtils
from ...models.subscription_feed_model import SubscriptionFeeds
from ...serializers.suscription_feed_serializer import SubscriptionFeedHelper


class SubscriptionFeedTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.rss_url = "https://urlfalsadelfeedparser.com"
        cls.test_helper = TestUtils()

    @patch.object(SubscriptionFeedHelper, 'parse_data')
    def test_authenticated_user_can_create_subscriptionFeed(self, url_parser):
        mock_value = {'link': 'https://falseurl.com', 'title': "Mom"}
        url_parser.return_value = mock_value
        self.test_helper.create_and_login_user('newuser', self.client)
        data = {"link": self.rss_url}
        resp = self.client.post("/main_app/feed/", data)

        self.assertEqual(resp.status_code, HTTPStatus.CREATED)
        self.assertEqual(len(SubscriptionFeeds.objects.filter(**mock_value)), 1)

    def test_feed_is_assigned_only_to_authenticated_user(self):
        data = {"link": self.rss_url}
        resp = self.client.post("/main_app/feed/", data)
        self.assertEqual(resp.status_code, HTTPStatus.UNAUTHORIZED)
        self.assertEqual(len(SubscriptionFeeds.objects.filter()), 0)

    def test_cannot_create_feed_using_invalid_url(self):
        self.test_helper.create_and_login_user('newuser1', self.client)
        data = {"link": "https://kako.com"}
        resp = self.client.post("/main_app/feed/", data)
        self.assertEqual(resp.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(resp.data['message'], 'Impossible to parse URL.')
        self.assertEqual(len(SubscriptionFeeds.objects.all()), 0)

    @patch.object(SubscriptionFeedHelper, 'parse_data')
    def test_two_user_creating_new_feed_only_creates_one(self, url_parser):
        url_parser.return_value = self.test_helper.false_subscription
        self.test_helper.submit_post_creating_user('newuser2', {"link": self.rss_url}, self.client)
        self.test_helper.submit_post_creating_user('newuser1', {"link": self.rss_url}, self.client)

        user1 = User.objects.filter(username='newuser2')[0]
        user2 = User.objects.filter(username='newuser1')[0]

        self.assertEqual(len(SubscriptionFeeds.objects.all()), 1)

        self.assertEqual(len(SubscriptionFeeds.objects.filter(users_subscribed=user1)), 1)
        self.assertEqual(len(SubscriptionFeeds.objects.filter(users_subscribed=user2)), 1)

    @patch.object(SubscriptionFeedHelper, 'parse_data')
    def test_createFeed_response_includes_information_of_the_model(self, url_parser):
        url_parser.return_value = self.test_helper.false_subscription
        self.test_helper.create_and_login_user('newuser1', self.client)
        data = {"link": self.rss_url}
        resp = self.client.post("/main_app/feed/", data).json()

        self.assertEqual(resp['link'], 'https://falseurl.com')
        self.assertEqual(resp['title'], 'Mom')
        self.assertEqual(resp['image'], None)

    @patch.object(SubscriptionFeedHelper, 'parse_data')
    def test_user_can_not_subscribe_twice_to_a_feed(self, url_parser):
        url_parser.return_value = self.test_helper.false_subscription
        self.test_helper.create_and_login_user('newuser1', self.client)
        data = {"link": self.rss_url}
        self.client.post("/main_app/feed/", data)
        resp = self.client.post("/main_app/feed/", data)
        self.assertEqual(resp.data['message'], 'User is already subscribed to that page.')

    @patch.object(SubscriptionFeedHelper, 'parse_data')
    def test_user_can_receives_her_subscriptions_using_get_request(self, url_parser):
        url_parser.return_value = self.test_helper.false_subscription
        self.test_helper.create_and_login_user('newuser1', self.client)
        data = {"link": self.rss_url}
        self.client.post("/main_app/feed/", data)
        resp = self.client.get("/main_app/feed/").json()

        self.assertEqual(resp[0]['link'], 'https://falseurl.com')
        self.assertEqual(resp[0]['title'], 'Mom')
        self.assertEqual(resp[0]['image'], None)
        self.assertEqual(resp[0]['id'], 1)

    @patch.object(SubscriptionFeedHelper, 'parse_data')
    def test_users_cannot_receives_subscriptions_of_other_users(self, url_parser):
        mock_value = {'link': 'https://falseurl1.com', 'title': "Mom1", 'image': 'miimagen.com', }
        url_parser.return_value = mock_value
        self.test_helper.submit_post_creating_user('newuser1', {"link": self.rss_url}, self.client)

        mock_value = {'link': 'https://falseurl2.com', 'title': "Mom2", 'image': 'miimagen.com', }
        url_parser.return_value = mock_value

        self.test_helper.submit_post_creating_user('newuser2', {"link": self.rss_url}, self.client)
        resp = self.client.get("/main_app/feed/").json()
        self.assertEqual(resp[0]['link'], 'https://falseurl2.com')
        self.assertEqual(resp[0]['title'], 'Mom2')
        self.assertEqual(resp[0]['image'], None)
        self.assertEqual(len(resp), 1)

