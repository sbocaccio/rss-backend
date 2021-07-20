from rest_framework.test import APITestCase
from http import HTTPStatus
from ...models.subscription_feed_model import SubscriptionFeeds
import mock
from mock import patch
from ...serializers.suscription_feed_serializer import FeedHelper, CreateFeedSerializers
from django.contrib.auth.models import User
from django.core import serializers
class SubscriptionFeedTest(APITestCase): 

    @classmethod
    def setUpTestData(cls):
        cls.rss_url = "https://urlfalsadelfeedparser.com"

    def create_and_login_user(self, username):
            data = {"username": username, "password": 'password123' ,"email": 'newuser@gmail.com'}
            resp= self.client.post('/main_app/register/', data)
            token = resp.json().get('access')
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)


    def submit_post_creating_user_and_mock(self,username):
        self.create_and_login_user(username)
        data = {"link": self.rss_url}
        self.client.post("/main_app/feed/", data)
        
    @patch.object(FeedHelper, 'parse_data')
    def test_authenticated_user_can_create_subscriptionFeed(self,mock_my_method):
            mock_value = {'link': 'https://falseurl.com', 'title': "Mom"}
            mock_my_method.return_value = mock_value
            self.create_and_login_user('newuser')
            data = {"link": self.rss_url}
            resp= self.client.post("/main_app/feed/", data)

            self.assertEqual(resp.status_code, HTTPStatus.CREATED )
            self.assertEqual(len(SubscriptionFeeds.objects.filter(**mock_value)),1)
        
    def test_feed_is_assigned_only_to_authenticated_user(self):
            data = {"link": self.rss_url}
            resp= self.client.post("/main_app/feed/", data)
            self.assertEqual(resp.status_code, HTTPStatus.UNAUTHORIZED )
            self.assertEqual(len(SubscriptionFeeds.objects.filter()) , 0)

    def test_cannot_create_feed_using_invalid_url(self):
            self.create_and_login_user('newuser1')
            data = {"link": "https://kako.com"}
            resp= self.client.post("/main_app/feed/", data)
            self.assertEqual(resp.status_code, HTTPStatus.BAD_REQUEST)
            self.assertEqual(resp.data['message'], 'Impossible to parse URL.')
            self.assertEqual(len(SubscriptionFeeds.objects.all()), 0)


    @patch.object(FeedHelper, 'parse_data')
    def test_two_user_creating_new_feed_only_creates_one(self,mock_my_method):
            mock_value = {'link': 'https://falseurl.com', 'title': "Mom", 'image': 'miimagen.com', }
            mock_my_method.return_value = mock_value
            self.submit_post_creating_user_and_mock('newuser2')
            self.submit_post_creating_user_and_mock('newuser1')

            user1 = User.objects.filter(username='newuser2')[0]
            user2 = User.objects.filter(username='newuser1')[0]

            self.assertEqual(len(SubscriptionFeeds.objects.all()), 1)

            self.assertEqual(len(SubscriptionFeeds.objects.filter(users_subscribed = user1 )),1)
            self.assertEqual(len(SubscriptionFeeds.objects.filter(users_subscribed=user2)), 1)


    @patch.object(FeedHelper, 'parse_data')
    def test_createFeed_response_includes_information_of_the_model(self,mock_my_method):
        mock_value = {'link': 'https://falseurl.com', 'title': "Mom", 'image': 'miimagen.com',}
        mock_my_method.return_value = mock_value
        self.create_and_login_user('newuser1')
        data = {"link": self.rss_url}
        resp = self.client.post("/main_app/feed/", data).json()


        self.assertEqual(resp['link'],'https://falseurl.com')
        self.assertEqual(resp['title'], 'Mom')
        self.assertEqual(resp['image'], None)

    @patch.object(FeedHelper, 'parse_data')
    def test_user_can_not_subscribe_twice_to_a_feed(self,mock_my_method):
        mock_value = {'link': 'https://falseurl.com', 'title': "Mom", 'image': 'miimagen.com', }
        mock_my_method.return_value = mock_value
        self.create_and_login_user('newuser1')
        data = {"link": self.rss_url}
        self.client.post("/main_app/feed/", data)
        resp = self.client.post("/main_app/feed/", data)
        self.assertEqual(resp.data['message'], 'User is already subscribed to that page.')

    @patch.object(FeedHelper, 'parse_data')
    def test_user_can_receives_her_subscriptions_using_api(self,mock_my_method):
        mock_value = {'link': 'https://falseurl.com', 'title': "Mom", 'image': 'miimagen.com', }
        mock_my_method.return_value = mock_value
        self.create_and_login_user('newuser1')
        data = {"link": self.rss_url}
        self.client.post("/main_app/feed/", data).json()
        resp =self.client.get("/main_app/feed/").json()

        self.assertEqual(resp[0]['link'], 'https://falseurl.com')
        self.assertEqual(resp[0]['title'], 'Mom')
        self.assertEqual(resp[0]['image'], None)

    @patch.object(FeedHelper, 'parse_data')
    def test_users_cannot_receives_subscriptions_of_other_users(self,mock_my_method):
        

        mock_value = {'link': 'https://falseurl1.com', 'title': "Mom1", 'image': 'miimagen.com', }
        mock_my_method.return_value = mock_value
        self.submit_post_creating_user_and_mock('newuser1')

        mock_value = {'link': 'https://falseurl2.com', 'title': "Mom2", 'image': 'miimagen.com', }
        mock_my_method.return_value = mock_value
        self.submit_post_creating_user_and_mock('newuser2')

        resp = self.client.get("/main_app/feed/").json()
        self.assertEqual(resp[0]['link'], 'https://falseurl2.com')
        self.assertEqual(resp[0]['title'], 'Mom2')
        self.assertEqual(resp[0]['image'], None)
        self.assertEqual(len(resp),1)

    def test_specific_page(self):
        self.create_and_login_user('newuser1')
        data = {"link": 'http://rss.cnn.com/rss/edition_us.rss'}
        self.client.post("/main_app/feed/", data).json()



