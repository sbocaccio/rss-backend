from ..models.subscription_feed_model import SubscriptionFeed
from rest_framework import  serializers


class CreateFeedSerializers(serializers.ModelSerializer):
    url = serializers.CharField(max_length=255)
    user_id = serializers.IntegerField(min_value = 1)
    class Meta:
        model = SubscriptionFeed
        fields = ['url','user_id']

    def create(self, validated_data):
        feed = SubscriptionFeed.objects.create(url = validated_data['url'], user_id = validated_data['user_id'])
        return feed
    