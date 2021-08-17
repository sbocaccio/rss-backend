
from http import HTTPStatus
from rest_framework import serializers

from .user_article_helper import UserArticleHelper
from ...models.subscription_feed_model import SubscriptionFeeds
from ...models.user_article import UserArticle
from ...models.user_folder import UserFolder


class UserFolderHelper():

    def create_folder(self, data,user):
        subscription = SubscriptionFeeds.objects.get(id=data['subscription'])
        name = data['name']
        user_folder, created = UserFolder.objects.get_or_create(name=name,user= user)
        user_folder.subscriptions_feed.add(subscription)
        user_folder.save()
        return user_folder