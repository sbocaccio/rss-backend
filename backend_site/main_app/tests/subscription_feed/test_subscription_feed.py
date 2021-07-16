from rest_framework.test import APITestCase
from http import HTTPStatus
from ...models.subscription_feed_model import SubscriptionFeed
import mock
from mock import patch
from ...serializers.suscription_feed_serializer import FeedHelper

class SubscriptionFeedTest(APITestCase): 

    @classmethod
    def setUpTestData(cls):
        cls.rss_url = "https://urlfalsadelfeedparser.com"

    def create_user(self, username):
            data = {"username": username, "password": 'password123' ,"email": 'newuser@gmail.com'}
            resp= self.client.post('/main_app/register/', data)
            token = resp.json().get('access')
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
            return resp.data['user_id']

    @patch.object(FeedHelper, 'parse_data')
    def test_authenticated_user_can_create_subscriptionFeed(self,mock_my_method):
            mock_value = {'link': 'https://falseurl.com', 'title': "Mom"}
            mock_my_method.return_value = mock_value
            self.create_user('newuser')
            data = {"url": self.rss_url}
            resp= self.client.post("/main_app/create_feed/", data)

            self.assertEqual(resp.status_code, HTTPStatus.OK )
            self.assertEqual(resp.data['message'],'Succesfully created feed.')
            self.assertEqual(len(SubscriptionFeed.objects.filter(**mock_value)),1)
        
    def test_none_authenticated_user_can_not_create_feed(self):
            data = {"url": self.rss_url}
            resp= self.client.post("/main_app/create_feed/", data)
            self.assertEqual(resp.status_code, HTTPStatus.UNAUTHORIZED )
            self.assertEqual(len(SubscriptionFeed.objects.filter()) , 0)

    @patch.object(FeedHelper, 'parse_data')
    def test_create_feed_has_user_id_field(self,mock_my_method):
            mock_value = {'link': 'https://falseurl.com', 'title': "Mom"}
            mock_my_method.return_value = mock_value
            user_id = self.create_user('newuser')
            data = {"url": self.rss_url}
            resp= self.client.post("/main_app/create_feed/", data)
            self.assertEqual(resp.status_code, HTTPStatus.OK )
            self.assertEqual(len(SubscriptionFeed.objects.filter(users_subscribed = user_id)), 1)
            self.assertEqual(len(SubscriptionFeed.objects.filter(users_subscribed = (user_id + 1) )), 0)

    def test_cannot_create_feed_using_invalid_url(self):
            user_id = self.create_user('newuser1')
            data = {"url": "https://kako.com"}
            resp= self.client.post("/main_app/create_feed/", data)
            self.assertEqual(resp.status_code, HTTPStatus.BAD_REQUEST)
            self.assertEqual(resp.data['message'], 'Impossible to parse URL.')
            self.assertEqual(len(SubscriptionFeed.objects.all()), 0)

    @patch.object(FeedHelper, 'parse_data')
    def test_two_user_creating_new_feed_only_creates_only(self,mock_my_method):
            mock_value = {'link': 'https://falseurl.com', 'title': "Mom"}
            mock_my_method.return_value = mock_value
            user1 = self.create_user('newuser1')
            data = {"url": self.rss_url}
            self.client.post("/main_app/create_feed/", data)

            user2 = self.create_user('newuser2')
            data = {"url": self.rss_url}
            self.client.post("/main_app/create_feed/", data)
            self.assertEqual(len(SubscriptionFeed.objects.all()), 1)

    @patch.object(FeedHelper, 'parse_data')
    def test_createFeed_response_includes_information_of_the_model(self,mock_my_method):
        mock_value = {'link': 'https://falseurl.com', 'title': "Mom", 'image': 'miimagen.com',}
        mock_my_method.return_value = mock_value
        user1 = self.create_user('newuser1')
        data = {"url": self.rss_url}
        resp = self.client.post("/main_app/create_feed/", data).data
        self.assertEqual(resp['title'] ,"Mom")
        self.assertEqual(resp['link'], "https://falseurl.com")
        self.assertEqual(resp['image'], "miimagen.com")


 