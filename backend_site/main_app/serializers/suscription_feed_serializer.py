import os
import urllib.request
from django.core.files import File
from os import error
from rest_framework import serializers

from ..auxiliary.helpers.feed_helper import SubscriptionFeedHelper
from ..auxiliary.helpers.user_article_helper import UserArticleHelper
from ..models.subscription_feed_model import SubscriptionFeeds
from ..models.user_folder import UserFolder



class CreateFeedSerializers(serializers.ModelSerializer):
    link = serializers.URLField(max_length=255)
    folders = serializers.SerializerMethodField()

    def get_folders(self, subscription):
        return UserFolder.objects.filter(subscriptions_feed__id=subscription.id, user= self.context['request'].user).values_list('name',flat = True)
    class Meta:
        model = SubscriptionFeeds
        fields = ['link', 'title', 'image', 'id','folders']
        read_only_fields = ['title', 'image', 'id']
        lookup_field = 'id'

    def create(self, validated_data):
        subscription_helper = SubscriptionFeedHelper()
        user = self.context['request'].user
        parsed_data = subscription_helper.parse_data(validated_data)
        feed = subscription_helper.create_feed(parsed_data)
        subscription_helper.add_user_to_subscription(feed,user,parsed_data)
        return feed

