import argparse
import sys
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from rest_framework.serializers import ValidationError
from xml.etree import ElementTree

from ...auxiliary.exceptions.no_users_recieved_exception import NotUserReceived
from ...auxiliary.exceptions.user_already_subscribed_exception import UserAlreadySubscribedException
from ...auxiliary.helpers.feed_helper import SubscriptionFeedHelper
from ...auxiliary.exceptions.not_parseable_link_exception import NotParseableLinkExcepcion


class Command(BaseCommand):
    help = 'Parse OPML file with subscriptions and add users to them.'

    def add_arguments(self, parser):
        parser.add_argument('file', type=str)
        parser.add_argument('users', nargs='*', type=str, default=[])
        parser.add_argument('--all', help='Add all users to the subscriptions.', action='store_const', const=True)

    def handle(self, *args, **options):
        users = self.get_users(options['users'], options['all'])
        file = options['file']
        feeds = self.OPML_parse(file)
        subscription_helper = SubscriptionFeedHelper()
        self.create_subscriptions(feeds, subscription_helper, users)

    def create_subscriptions(self, feeds, subscription_helper, users):
        for feed in feeds:
            try:
                feed_link = {'link':feed}
                subscription = subscription_helper.create_feed(feed_link)
                self.add_users_to_subscription(subscription,subscription_helper, users)
            except NotParseableLinkExcepcion as error:
                self.stdout.write(self.style.ERROR('ERROR: %s' % error.detail))

    def add_users_to_subscription(self, subscription,subscription_helper,users):
            self.stdout.write('Adding users to subscription %s' % subscription.title)
            added_users, not_added_used = subscription_helper.add_many_users_to_subscription(subscription, users)
            for user in added_users:
                self.stdout.write(self.style.SUCCESS('Successfully added user "%s" to subscription ' % user))
            for user, error in not_added_used:
                self.stdout.write(self.style.ERROR('ERROR: %s' % error.detail))

    def add_user_to_subscription(self, subscription, subscription_helper, user,subscription_parsed_data):
        self.stdout.write('Adding %s to subscription' % user.username)
        subscription_helper.add_user_to_subscription(subscription, user,subscription_parsed_data)

    def OPML_parse(self, file):
        urls = []
        with open(file, 'rt') as f:
            tree = ElementTree.parse(f)
        for node in tree.findall('.//outline'):
            url = node.attrib.get('xmlUrl')
            if url:
                urls.append(url)
        return urls

    def get_users(self, usernames, all_user_activated):
        self.stdout.write('Starting to retrieve users from database')
        users = None
        if (all_user_activated):
            users = list(User.objects.all())
        else:
            users = self._get_valid_users(usernames)
        if (not users):
            raise NotUserReceived()
        self.stdout.write('Retrieving users completed')
        return users

    def _get_valid_users(self, usernames):
        valid_users = []
        for user in usernames:
            try:
                user = User.objects.get(username=user)
                valid_users.append(user)
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(
                    'ERROR: %s is not registered so is not going to be add to any subscription' % user))
        return valid_users
