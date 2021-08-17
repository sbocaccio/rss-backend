
from http import HTTPStatus
from rest_framework import serializers

from .user_article_helper import UserArticleHelper
from ...models.subscription_feed_model import SubscriptionFeeds
from ...models.user_article import UserArticle
from ...models.user_folder import UserFolder
from ..exceptions.already_created_folder_exception import AlreadyCreatedFolder


class UserFolderHelper():

    def create_folder(self, name,user):
        user_folder, created = UserFolder.objects.get_or_create(name=name,user= user)
        if(not created):
            raise AlreadyCreatedFolder()
        user_folder.save()
        return user_folder