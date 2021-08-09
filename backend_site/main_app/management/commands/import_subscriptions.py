import sys
from django.core.management.base import BaseCommand, CommandError
from xml.etree import ElementTree
from ...auxiliary.helpers.feed_helper import SubscriptionFeedHelper
from django.contrib.auth.models import User
from rest_framework.serializers import ValidationError
from termcolor import colored
import argparse
class Command(BaseCommand):
    help = 'Parse OPML file with subscriptions and add users to them.'
    def add_arguments(self, parser):
        parser.add_argument('file', type=str)
        parser.add_argument('users', nargs='+', type=str)

    def handle(self, *args, **options):
        users = self.getUser(options['users'])
        file = options['file']
        feeds = self.OPML_parse(file)
        subscription_helper = SubscriptionFeedHelper()
        for feed in feeds:
            for user in users:
                print(colored('START', 'green'), 'adding subscription to feed', feed)
                try :
                    self.add_user_to_subscription(feed, subscription_helper, user)
                except ValidationError as error:
                    print(colored('ERROR:','red'),error.detail['message'])
                except ValueError as error:
                    print(colored('ERROR:','red'),error)
                except Exception as error:
                    print(colored('ERROR:', 'red'), error)

                else:
                    print(colored('SUCCESS:','green'),'Successfully added user:', user, 'to subscription', feed)

    def add_user_to_subscription(self, feed, subscription_helper, user):
        print(colored('START', 'green'), 'adding', user.username, 'to subscription', feed)
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

    def getUser(self,usernames):
        users = []
        print(colored('Starting to retrieve users from database', 'yellow'))
        for user in usernames:
            try:
                print(manolo)
                user = User.objects.get(username=user)
                print(user)
                users.append(user)
            except:
                print(colored('ERROR', 'red'), 'user ', user, ' is not created so is going to be dismissed in adding it to the subscriptions')

        print(colored('Retrieving users completed', 'yellow'))
        return users

