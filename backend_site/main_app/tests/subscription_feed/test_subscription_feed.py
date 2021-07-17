from rest_framework.test import APITestCase
from rest_framework.test import APITestCase
from http import HTTPStatus
from ...models.subscription_feed_model import SubscriptionFeeds
import mock
from mock import patch
from ...serializers.suscription_feed_serializer import FeedHelper
from django.contrib.auth.models import User

class SubscriptionFeedTest(APITestCase): 

    @classmethod
    def setUpTestData(cls):
        cls.rss_url = "https://urlfalsadelfeedparser.com"

    def create_and_login_user(self, username):
            data = {"username": username, "password": 'password123' ,"email": 'newuser@gmail.com'}
            resp= self.client.post('/main_app/register/', data)
            token = resp.json().get('access')
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    @patch.object(FeedHelper, 'parse_data')
    def test_authenticated_user_can_create_subscriptionFeed(self,mock_my_method):
            mock_value = {'link': 'https://falseurl.com', 'title': "Mom"}
            mock_my_method.return_value = mock_value
            self.create_and_login_user('newuser')
            data = {"get_or_create": self.rss_url}
            resp= self.client.post("/main_app/create_feed/", data)

            self.assertEqual(resp.status_code, HTTPStatus.OK )
            self.assertEqual(resp.data['message'],'Succesfully created feed.')
            self.assertEqual(len(SubscriptionFeeds.objects.filter(**mock_value)),1)
        
    def test_none_authenticated_user_can_not_create_feed(self):
            data = {"get_or_create": self.rss_url}
            resp= self.client.post("/main_app/create_feed/", data)
            self.assertEqual(resp.status_code, HTTPStatus.UNAUTHORIZED )
            self.assertEqual(len(SubscriptionFeeds.objects.filter()) , 0)

    def test_cannot_create_feed_using_invalid_url(self):
            user_id = self.create_and_login_user('newuser1')
            data = {"get_or_create": "https://kako.com"}
            resp= self.client.post("/main_app/create_feed/", data)
            self.assertEqual(resp.status_code, HTTPStatus.BAD_REQUEST)
            self.assertEqual(resp.data['message'], 'Impossible to parse URL.')
            self.assertEqual(len(SubscriptionFeeds.objects.all()), 0)

    @patch.object(FeedHelper, 'parse_data')
    def test_two_user_creating_new_feed_only_creates_only(self,mock_my_method):
            mock_value = {'link': 'https://falseurl.com', 'title': "Mom"}
            mock_my_method.return_value = mock_value
            self.create_and_login_user('newuser1')
            data = {"get_or_create": self.rss_url}
            self.client.post("/main_app/create_feed/", data)

            self.create_and_login_user('newuser2')
            data = {"get_or_create": self.rss_url}
            self.client.post("/main_app/create_feed/", data)

            self.assertEqual(len(SubscriptionFeeds.objects.all()), 1)
            user1 = User.objects.filter(username='newuser2')[0]
            user2 = User.objects.filter(username='newuser1')[0]
            self.assertEqual(len(SubscriptionFeeds.objects.filter(users_subscribed = user2 )),1)
            self.assertEqual(len(SubscriptionFeeds.objects.filter(users_subscribed = user1 )),1)


    @patch.object(FeedHelper, 'parse_data')
    def test_createFeed_response_includes_information_of_the_model(self,mock_my_method):
        mock_value = {'link': 'https://falseurl.com', 'title': "Mom", 'image': 'miimagen.com',}
        mock_my_method.return_value = mock_value
        user1 = self.create_and_login_user('newuser1')
        data = {"get_or_create": self.rss_url}
        resp = self.client.post("/main_app/create_feed/", data).data
        self.assertEqual(resp['title'] ,"Mom")
        self.assertEqual(resp['link'], "https://falseurl.com")
        self.assertEqual(resp['image'], "miimagen.com")

