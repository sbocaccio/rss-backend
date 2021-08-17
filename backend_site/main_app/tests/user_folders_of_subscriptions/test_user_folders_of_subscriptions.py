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
        resp = self.client.post('/main_app/folder',data)
        user_folder = UserFolder.objects.get()
        self.assertEquals(user_folder.user.username, 'newuser')
        self.assertEquals(user_folder.name, 'folder_name')
        self.assertEquals(UserFolder.objects.all().count(),1)
        self.assertEquals(resp.status_code, HTTPStatus.CREATED)


    @patch.object(SubscriptionFeedHelper, 'parse_data')
    def test_user_can_add_a_subscription_to_a_folder(self, url_parser):
        url_parser.return_value = self.test_helper.false_subscription
        subscription = self.test_helper.submit_post_creating_user('newuser', {"link": self.rss_url}, self.client).data['id']
        data = {'name': self.folder_name}
        folder_pk =self.client.post('/main_app/folder', data).json()['pk']
        data = {'subscription_id':subscription}
        resp = self.client.put('/main_app/folder/' + str(folder_pk), data)
        user_folder = UserFolder.objects.get()
        assert(subscription in user_folder.subscriptions_feed.all().values_list('id',flat = True))

    def test_user_can_not_add_a_subscription_to_a_non_existent_folder(self):
        self.test_helper.create_and_login_user('newuser',self.client)
        data = {'subscription_id': '1234'}
        resp = self.client.put('/main_app/folder/123', data)
        self.assertEquals(resp.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEquals(resp.data['detail'], 'This folder does not exist or is not part of any of your folders')

    def test_user_can_not_add_a_non_existent_subscription_to_a_folder(self):
        self.test_helper.create_and_login_user('newuser', self.client)
        data = {'name': self.folder_name}
        folder_pk = self.client.post('/main_app/folder', data).json()['pk']
        data = {'subscription_id': '1234'}
        resp = self.client.put('/main_app/folder/' + str(folder_pk), data)
        self.assertEquals(resp.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEquals(resp.data['detail'], 'You are not subscribed to that feed. Subscribe first.')

    def test_user_can_not_create_an_already_created_folder(self):
        self.test_helper.create_and_login_user('newuser', self.client)
        data = {'name': self.folder_name}
        self.client.post('/main_app/folder', data)
        resp = self.client.post('/main_app/folder', data)
        self.assertEquals(resp.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEquals(resp.data['detail'], 'This folder is already created. You cannot create it twice.')

    @patch.object(SubscriptionFeedHelper, 'parse_data')
    def test_user_can_add_a_subscription_to_a_folder_twice(self, url_parser):
        url_parser.return_value = self.test_helper.false_subscription
        subscription = self.test_helper.submit_post_creating_user('newuser', {"link": self.rss_url}, self.client).data[
            'id']
        data = {'name': self.folder_name}
        folder_pk = self.client.post('/main_app/folder', data).json()['pk']
        data = {'subscription_id': subscription}
        self.client.put('/main_app/folder/' + str(folder_pk), data)
        resp = self.client.put('/main_app/folder/' + str(folder_pk), data)
        user_folder = UserFolder.objects.get()
        assert (subscription in user_folder.subscriptions_feed.all().values_list('id', flat=True))

    @patch.object(SubscriptionFeedHelper, 'parse_data')
    def test_user_can_add_a_subscription_to_two_folders(self, url_parser):
        url_parser.return_value = self.test_helper.false_subscription
        subscription = self.test_helper.submit_post_creating_user('newuser', {"link": self.rss_url}, self.client).data[
            'id']

        folder1 = {'name': self.folder_name}
        folder_pk = self.client.post('/main_app/folder', folder1).json()['pk']
        data = {'subscription_id': subscription}
        self.client.put('/main_app/folder/' + str(folder_pk), data)

        folder2 = {'name': 'another_folder'}
        folder_pk = self.client.post('/main_app/folder', folder2).json()['pk']
        data = {'subscription_id': subscription}
        self.client.put('/main_app/folder/' + str(folder_pk), data)
        resp = self.client.put('/main_app/folder/' + str(folder_pk), data)

        user_folders = UserFolder.objects.all()
        self.assertEquals(user_folders.count(), 2)
        assert (subscription in user_folders[0].subscriptions_feed.all().values_list('id', flat=True))
        assert (subscription in user_folders[1].subscriptions_feed.all().values_list('id', flat=True))
