
from rest_framework.test import APITestCase, APIClient
from ...serializers.suscription_feed_serializer import FeedHelper
from mock import patch
from ...models.article import Article
from django.contrib.auth.models import User


class DisplayArticulesTest(APITestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.rss_url = "https://urlfalsadelfeedparser.com"



    def create_and_login_user(self, username):
            data = {"username": username, "password": 'password123' ,"email": 'newuser@gmail.com'}
            resp= self.client.post('/main_app/register/', data)
            token = resp.json().get('access')
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)


    def submit_post_creating_user(self,username,data):
        self.create_and_login_user(username)
        self.client.post("/main_app/feed/", data)

    @patch.object(FeedHelper, 'parse_data')
    def test_create_a_post_generates_an_article(self,url_parser):
        mock_value = {'link': 'https://falseurl.com', 'title': "Mom", 'entries':[{'title': 'Titulo', 'link': 'linkfalso','summary': 'summaryfalso'}]}
        url_parser.return_value = mock_value
        self.submit_post_creating_user('newuser',{"link": self.rss_url})
        self.assertEqual(len(Article.objects.all()), 1)

    @patch.object(FeedHelper, 'parse_data')
    def test_articles_have_one_user_and_correct_data_when_they_are_created(self,url_parser):
        mock_value = {'link': 'https://falseurl.com', 'title': "Mom",'entries': [{'title': 'Titulo', 'link': 'linkfalso', 'summary': 'summaryfalso'}]}
        url_parser.return_value = mock_value
        self.submit_post_creating_user('newuser', {"link": self.rss_url})
        user1 = User.objects.filter(username='newuser')[0]
        articles = Article.objects.filter(users_subscribed=user1)
        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].title, 'Titulo')
        self.assertEqual(articles[0].link, 'linkfalso')
        self.assertEqual(articles[0].summary, 'summaryfalso')

    @patch.object(FeedHelper, 'parse_data')
    def test_articles_can_be_retrieved_passing_subscription_as_parameter(self, url_parser):
        mock_value = {'link': 'https://falseurl.com', 'title': "Mom",
                      'entries': [{'title': 'Titulo', 'link': 'linkfalso', 'summary': 'summaryfalso'}]}
        url_parser.return_value = mock_value
        self.submit_post_creating_user('newuser', {"link": self.rss_url})
        data = {'link':'https://falseurl.com', 'action':'refresh'}
        resp = self.client.get('/main_app/articles/', data= data).json()
        self.assertEqual(len(resp), 1)
        self.assertEqual(resp[0]['link'], 'linkfalso')
        self.assertEqual(resp[0]['title'],'Titulo' )
        self.assertEqual(resp[0]['summary'], 'summaryfalso')

    @patch.object(FeedHelper, 'parse_data')
    def test_user_can_not_receive_articles_of_a_subscription_is_not_subscribed(self, url_parser):
        mock_value = {'link': 'https://falseurl.com', 'title': "Mom",
                      'entries': [{'title': 'Titulo', 'link': 'linkfalso', 'summary': 'summaryfalso'}]}
        url_parser.return_value = mock_value
        self.submit_post_creating_user('newuser', {"link": ''})
        data = {'link':'https://falseurl2.com', 'action':'refresh'}
        resp = self.client.get('/main_app/articles/', data= data).json()
        self.assertEqual(resp['detail'], 'You are not subscribed to that feed. Subscribe first to read articles')



