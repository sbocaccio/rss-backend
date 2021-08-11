import os
import urllib.request
from django.core.files import File
from os import error
from rest_framework import serializers

from ..auxiliary.helpers.feed_helper import SubscriptionFeedHelper
from ..auxiliary.helpers.user_article_helper import UserArticleHelper
from ..models.subscription_feed_model import SubscriptionFeeds


class CreateFeedSerializers(serializers.ModelSerializer):
    link = serializers.URLField(max_length=255)

    class Meta:
        model = SubscriptionFeeds
        fields = ['link', 'title', 'image', 'id']
        read_only_fields = ['title', 'image', 'id']
        lookup_field = 'id'

    def create(self, validated_data):
        subscription_helper = SubscriptionFeedHelper()
        user = self.context['request'].user
        feed = subscription_helper.create_feed(validated_data,user)
      #  subscription_helper.add_user_to_subscription(feed.id,user)
        return feed

