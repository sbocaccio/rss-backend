import feedparser
from http import HTTPStatus
from rest_framework import serializers

from .user_article_helper import UserArticleHelper
from ...models.subscription_feed_model import SubscriptionFeeds
from ...models.user_article import UserArticle


class SubscriptionFeedHelper():
    def parse_data(self, data):
        feed_parse = self._assert_can_parse(data)
        parse_data = self._select_fields(data, feed_parse)
        return parse_data

    def _select_fields(self, data, feed_parse):
        parse_data = {}
        parse_data['link'] = data['link']
        parse_data['title'] = feed_parse.feed['title']
        if ('entries' in feed_parse):
            parse_data['entries'] = feed_parse['entries']
        if ('image' in feed_parse.feed):
            parse_data['image'] = feed_parse.feed['image']['href']
        return parse_data

    def _assert_can_parse(self, data):
        feed_parse = feedparser.parse(data['link'])
        if (not 'status' in feed_parse or feed_parse['status'] != HTTPStatus.OK or not 'title' in feed_parse.feed):
            raise AttributeError('Impossible to parse URL.')
        return feed_parse

    def update_subscription(self, subscription, user):
        subscription_link = {"link": subscription.link}
        parsed_data = self._parse_data(subscription_link)
        articles, new_articles_cant = self._update_articles_for_subscription(subscription, parsed_data, user)
        if articles:
            subscription.subscription_articles.add(*articles)
            subscription.save()

        user_article_helper = UserArticleHelper()
        user_article_helper.remove_old_user_articles_from_subscription_and_user(subscription, user)
        updated_articles = UserArticle.objects.all_user_articles_from_user_and_subscription_sorted_in_descending_date_order(
            user, subscription)
        return updated_articles, new_articles_cant
    def _update_articles_for_subscription(self, subscription, parsed_data, user):
        if ('entries' in parsed_data):
            user_article_helper = UserArticleHelper()
            newest_articles = parsed_data['entries'][0:(min(10, len(parsed_data['entries'])))]
            articles, new_articles_cant = user_article_helper.create_user_articles(newest_articles, subscription, user)
            return articles, new_articles_cant

    def _create_feed(self, validated_data, user):
        parsed_data = self._parse_data(validated_data)
        subscription = self._get_or_create_subscription_model(parsed_data, user)[0]
        subscription.users_subscribed.add(user)
        articles = self._create_articles_for_subscription(subscription, parsed_data, user)
        if articles:
            subscription.subscription_articles.add(*articles)
        subscription.save()
        return subscription

    def _get_or_create_subscription_model(self, parsed_data, user):
        result = None
        if ('image' in parsed_data):
            try:
                result = urllib.request.urlretrieve(parsed_data['image'])
            except:
                parsed_data['image'] = ''
        subscription, created = SubscriptionFeeds.objects.get_or_create(link=parsed_data['link'])
        subscription.title = parsed_data['title']
        if SubscriptionFeeds.objects.filter(users_subscribed=user, id=subscription.id):
            error = serializers.ValidationError({'message': 'User is already subscribed to that page.'})
            error.status_code = '409'
            raise error
        if ('image' in parsed_data and parsed_data['image']):
            subscription.image.save(
                os.path.basename(parsed_data['link']),
                File(open(result[0], 'rb'))
            )
        return subscription, created

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
            articles, new_articles_cant = user_article_helper.create_user_articles(last_articles, subscription, user)
            return articles
