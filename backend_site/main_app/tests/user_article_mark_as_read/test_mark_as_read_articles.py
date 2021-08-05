from mock import patch
from rest_framework.test import APITestCase, APIClient

from ...serializers.suscription_feed_serializer import SubscriptionFeedHelper
from ...auxiliary.helpers.test_helper import TestUtils


class UserArticleReadStateTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.rss_url = "https://urlfalsadelfeedparser.com"
        cls.test_helper = TestUtils()

    @patch.object(SubscriptionFeedHelper, 'parse_data')
    def test_user_article_state_start_being_false(self, url_parser):
        url_parser.return_value = self.test_helper.false_subscription
        self.test_helper.submit_post_creating_user('newuser', {"link": self.rss_url}, self.client)
        resp = self.client.get('/main_app/subscriptions/1/articles/').data
        self.assertEqual(resp[0]['read'] , False)

