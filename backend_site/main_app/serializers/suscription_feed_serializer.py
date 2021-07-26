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

    def create(self, validated_data):
        feed = self._create_feed(validated_data)
        return feed

    def _create_feed(self, validated_data):
        parsed_data = self._parse_data(validated_data)
        user = self.context['request'].user
        result = None
        if ('image' in parsed_data):
            try:
                result = urllib.request.urlretrieve(parsed_data['image'])
            except:
                parsed_data['image'] = ''

        subscription, created = SubscriptionFeeds.objects.get_or_create(link=parsed_data['link'],
                                                                        title=parsed_data['title'])

        if (user in subscription.users_subscribed.all()):
            error = serializers.ValidationError({'message': 'User is already subscribed to that page.'})
            error.status_code = '409'
            raise error

        if ('image' in parsed_data and parsed_data['image']):
            subscription.image.save(
                os.path.basename(parsed_data['link']),
                File(open(result[0], 'rb'))
            )

        subscription.users_subscribed.add(user)
        articles = self._create_articles_for_subscription(subscription, parsed_data, user)
        if articles:
            for articles in articles:
                subscription.subscription_articles.add(articles)

        return subscription

    def _parse_data(self, validated_data):
        try:
            feed_helper = SubscriptionFeedHelper()
            parse_data = feed_helper.parse_data(validated_data)
        except AttributeError as error:
            raise serializers.ValidationError({'message': error}, code='400')
        return parse_data

    def _create_articles_for_subscription(self, subscription, parsed_data, user):
        if ('entries' in parsed_data):
            user_article_helper = UserArticleHelper()
            last_articles = parsed_data['entries'][0:(min(10, len(parsed_data['entries'])))]
            articles =  user_article_helper.create_user_articles(last_articles, subscription, user)
            return articles
