from mock import patch
from rest_framework.test import APITestCase, APIClient

from ...models.user_folder import UserFolder
from ...serializers.suscription_feed_serializer import SubscriptionFeedHelper
from ...auxiliary.helpers.test_helper import TestUtils
from http import HTTPStatus


class UserFolderTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.rss_url = "https://urlfalsadelfeedparser.com"
        cls.test_helper = TestUtils()
        cls.folder_name = 'folder_name'


    def test_user_can_create_a_folder(self):

        self.test_helper.create_and_login_user('newuser',self.client)
        data = {'name': self.folder_name}
        resp = self.client.post('/main_app/folder/',data)
        user_folder = UserFolder.objects.get()
        self.assertEquals(user_folder.user.username, 'newuser')
        self.assertEquals(user_folder.name, 'folder_name')
        self.assertEquals(UserFolder.objects.all().count(),1)
        self.assertEquals(resp.status_code, HTTPStatus.CREATED)

    '''
    @patch.object(SubscriptionFeedHelper, 'parse_data')
    def test_user_can_add_a_subscription_to_a_folder(self, url_parser):
        url_parser.return_value = self.test_helper.false_subscription
        subscription = self.test_helper.submit_post_creating_user('newuser', {"link": self.rss_url}, self.client).data[
            'id']
        data = {'name': self.folder_name, 'subscription': subscription}
        resp = self.client.post('/main_app/folder/', data)
        user_folder = UserFolder.objects.get()
        self.assertEquals(user_folder.user.username, 'newuser')
        self.assertEquals(user_folder.name, 'folder_name')
        assert (subscription in user_folder.subscriptions_feed.all().values_list('id', flat=True))
        self.assertEquals(UserFolder.objects.all().count(), 1)
    '''

