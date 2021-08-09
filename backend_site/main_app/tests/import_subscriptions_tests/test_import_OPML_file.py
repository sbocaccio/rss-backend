from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from django.core.management import BaseCommand, CommandError
from io import StringIO
from django.core.management import call_command
from ...models.subscription_feed_model import SubscriptionFeeds
from mock import patch

class ImportOPMLFileSubscription(APITestCase):

    @patch.object(SubscriptionFeedHelper, 'parse_data')
    def test_command_create_subscription_for_existing_user_and_user_is_in(self):
        user = User.objects.create_user(username='username', password='password', email='email@email.com')
        call_command('import_subscriptions' ,'main_app/tests/import_subscriptions_tests/one_feed.opml', 'username')
        subscription =SubscriptionFeeds.objects.get()
        user_subscribed = list(subscription.users_subscribed)
        self.assertNotEqual(SubscriptionFeeds.objects.first(), None)
        self.assertEqual(user in user_subscribed, True)







