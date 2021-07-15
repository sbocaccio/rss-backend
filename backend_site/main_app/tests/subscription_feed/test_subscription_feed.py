from rest_framework.test import APITestCase
from http import HTTPStatus
from ...models.subscription_feed_model import SubscriptionFeed

 
class SubscriptionFeedTest(APITestCase): 

    @classmethod
    def setUpTestData(cls):
        cls.rss_url = 'http://example.com'

    def create_user(self):
            data = {"username": 'newuser', "password": 'password123' ,"email": 'newuser@gmail.com'}
            resp= self.client.post('/main_app/register/', data)
            token = resp.json().get('access')
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
            return resp.data['user_id']
    

    def test_authenticated_user_can_create_subscriptionFeed(self):

            user_id = self.create_user()
            data = {"url": self.rss_url}
            resp= self.client.post("/main_app/create_feed/", data)
            self.assertEqual(resp.status_code, HTTPStatus.OK )
            self.assertEqual(len(SubscriptionFeed.objects.all()) , 1)
            self.assertEqual(resp.data['message'],'Succesfully created feed.')
        
    def test_none_authenticated_user_can_not_create_feed(self):
            data = {"url": self.rss_url}
            resp= self.client.post("/main_app/create_feed/", data)
            self.assertEqual(resp.status_code, HTTPStatus.UNAUTHORIZED )
            self.assertEqual(len(SubscriptionFeed.objects.filter()) , 0)

    def test_create_feed_has_user_id_field(self):
            user_id = self.create_user()
            data = {"url": self.rss_url}
            resp= self.client.post("/main_app/create_feed/", data)
            self.assertEqual(resp.status_code, HTTPStatus.OK )
            self.assertEqual(len(SubscriptionFeed.objects.filter(user_id = user_id)), 1)
            self.assertEqual(len(SubscriptionFeed.objects.filter(user_id = (user_id + 1) )), 0)


