import argparse
import sys
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from rest_framework.serializers import ValidationError
from termcolor import colored
from xml.etree import ElementTree

from ...auxiliary.exceptions.no_users_recieved_exception import NotUserReceived
from ...auxiliary.helpers.feed_helper import SubscriptionFeedHelper

class Command(BaseCommand):
    help = 'Parse OPML file with subscriptions and add users to them.'

    def add_arguments(self, parser):
        parser.add_argument('file', type=str)
        parser.add_argument('users', nargs='*', type=str, default=[])
        parser.add_argument( '--all', help='Add all users to the subscriptions.',action='store_const', const=True)


    def handle(self, *args, **options):
        users = self.getUser(options['users'],options['all'])
        file = options['file']
        feeds = self.OPML_parse(file)
        subscription_helper = SubscriptionFeedHelper()
        self.create_subscriptions(feeds, subscription_helper, users)

    def create_subscriptions(self, feeds, subscription_helper, users):
        for feed in feeds:
            self.stdout.write('Adding users to subscription %s' % feed)
            for user in users:
                try:
                    self.add_user_to_subscription(feed, subscription_helper, user)
                except ValidationError as error:
                    self.stdout.write(self.style.ERROR('ERROR: %s' % error.detail['message']))
                else:
                    self.stdout.write(self.style.SUCCESS('Successfully added user "%s" to subscription ' % user))

    def add_user_to_subscription(self, feed, subscription_helper, user):
        self.stdout.write('Adding %s to subscription' % user.username)
        data = {'link': feed}
        subscription_helper.create_feed(data, user)

    def OPML_parse(self, file):
        urls = []
        with open(file, 'rt') as f:
            tree = ElementTree.parse(f)
        for node in tree.findall('.//outline'):
            url = node.attrib.get('xmlUrl')
            if url:
                urls.append(url)
        return urls

    def getUser(self, usernames,all_user_activated):
        self.stdout.write('Starting to retrieve users from database')
        users = []
        if(all_user_activated):
            users = list(User.objects.all())
        else:
            users = self._get_valid_users(usernames)
        if (not users):
            raise NotUserReceived()
        self.stdout.write('Retrieving users completed')
        return users

    def _get_valid_users(self, usernames):
        valid_users= []
        for user in usernames:
            try:
                user = User.objects.get(username=user)
                valid_users.append(user)
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(
                    'ERROR: %s is not registered so is not going to be add to any subscription' % user))
        return valid_users
