from os import error
from ..models.subscription_feed_model import SubscriptionFeeds
from rest_framework import  serializers
from ..auxiliary.feed_helper import FeedHelper

class CreateFeedSerializers(serializers.ModelSerializer):
    get_or_create = serializers.CharField(max_length=255)
    class Meta:
        model = SubscriptionFeeds
        fields = ['get_or_create']

    def create(self, validated_data):
        feed = self._create_feed(validated_data)
        return feed

    def _create_feed(self, validated_data):
        parsed_data = self._parse_data(validated_data)
        user = self.context['request'].user
        if (len(SubscriptionFeeds.objects.filter(**parsed_data)) == 0):
            feed = SubscriptionFeeds.objects.create(**parsed_data)
        else:
            feed = SubscriptionFeeds.objects.filter(**parsed_data)[0]
        feed.users_subscribed.add(user)

        return feed

    def _parse_data(self, validated_data):
        try:
            feed_helper = FeedHelper()
            parse_data = feed_helper.parse_data(validated_data)
        except AttributeError as error:
            raise serializers.ValidationError({'message': error}, code='400')
        return parse_data
    