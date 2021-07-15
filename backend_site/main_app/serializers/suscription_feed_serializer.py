
from .models import SubscriptionFeed
from rest_framework import  serializers


class CreateFeedSerializers(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionFeed
        fields = ['url']
    def create(self, validated_data):
        feed = SubscriptionFeed.objects.create(url = validated_data['url'])
        return feed
