from os import error
from ..models.subscription_feed_model import SubscriptionFeeds
from rest_framework import  serializers
import feedparser
from http import HTTPStatus

class FeedHelper():
    feed_parse = {}
    def parse_data(self, data):
        parse_data = {}
        self._assert_can_parse(data)
        self._add_fields(data, parse_data)
        return parse_data

    def _add_fields(self, data, parse_data):
        parse_data['link'] = data['get_or_create']
        parse_data['title'] = self.feed_parse.feed['title']
        if ('image' in self.feed_parse.feed):
            parse_data['image'] = self.feed_parse.feed['image']['href']

    def _assert_can_parse(self, data):
        try:
            self.feed_parse = feedparser.parse(data['get_or_create'])
            if (self.feed_parse['status'] != HTTPStatus.OK):
                raise Exception()
        except:
            raise  AssertionError ('Impossible to parse URL.')
           
        return self.feed_parse


class CreateFeedSerializers(serializers.ModelSerializer):
    get_or_create = serializers.CharField(max_length=255)
    feed_helper = FeedHelper()
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
            parse_data = self.feed_helper.parse_data(validated_data)
        except AssertionError as error:
            raise serializers.ValidationError({'message': error}, code='400')
        return parse_data
    