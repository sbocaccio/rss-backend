from ..models.subscription_feed_model import SubscriptionFeed
from rest_framework import  serializers
import feedparser

class CreateFeedSerializers(serializers.ModelSerializer):
    url = serializers.CharField(max_length=255)
    user_id = serializers.IntegerField(min_value = 1)
    class Meta:
        model = SubscriptionFeed
        fields = ['url','user_id']

    def parse_data(self, data):
        parse_data = {}
        try:
            feed = feedparser.parse(data['url']).entries[1]
            parse_data['link'] = feed['link']
            parse_data['title'] = feed['title']
            parse_data['summary'] = feed['summary']
            return parse_data
        except:
            msg = ('Invalid url.')
            raise serializers.ValidationError({'message': msg}, code='400')

    def create(self, validated_data):
        parse_data = self.parse_data(validated_data)
        feed = SubscriptionFeed.objects.create(link = parse_data['link'], user_id = validated_data['user_id'], title = parse_data['title'], summary = parse_data['summary'])
        return feed
    