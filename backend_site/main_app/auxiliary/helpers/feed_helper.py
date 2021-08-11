import feedparser
from http import HTTPStatus
from rest_framework import serializers

from .constants import MAX_PERMITTED_ARTICLES
from .user_article_helper import UserArticleHelper
from ..exceptions.user_already_subscribed_exception import UserAlreadySubscribedException
from ..exceptions.not_parseable_link_exception import NotParseableLinkExcepcion
from ...models.subscription_feed_model import SubscriptionFeeds
from ...models.user_article import UserArticle


class SubscriptionFeedHelper():

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

    def update_subscription_of_user(self, subscription, user):
        subscription_link = {"link": subscription.link}
        parsed_data = self.parse_data(subscription_link)
        articles, new_articles_cant = self._update_articles_for_subscription_of_user(subscription, parsed_data, user)
        if articles:
            subscription.subscription_articles.add(*articles)
            subscription.save()

        user_article_helper = UserArticleHelper()
        user_article_helper.remove_old_user_articles_from_subscription_and_user(subscription, user)
        updated_articles = UserArticle.objects.all_user_articles_from_user_and_subscription_sorted_in_descending_date_order(
            user, subscription)
        return updated_articles, new_articles_cant

    def _update_articles_for_subscription_of_user(self, subscription, parsed_data, user):
        if ('entries' in parsed_data):
            user_article_helper = UserArticleHelper()
            newest_articles = parsed_data['entries'][0:(min(MAX_PERMITTED_ARTICLES, len(parsed_data['entries'])))]
            articles, new_articles_cant = user_article_helper.create_user_articles(newest_articles, subscription, user)
            return articles, new_articles_cant

    def create_feed(self, subscription_parsed_data):
        subscription = self._get_or_create_subscription_model(subscription_parsed_data)[0]
        return subscription

    def add_user_to_subscription(self, subscription, user, subscription_parsed_data):
        if user in subscription.users_subscribed.all():
            raise UserAlreadySubscribedException()

        subscription.users_subscribed.add(user)
        articles = self._create_articles_for_subscription(subscription, subscription_parsed_data, user)
        if articles:
            subscription.subscription_articles.add(*articles)
        subscription.save()

    def _get_or_create_subscription_model(self, parsed_data):
        result = None
        if ('image' in parsed_data):
            try:
                result = urllib.request.urlretrieve(parsed_data['image'])
            except:
                parsed_data['image'] = ''
        subscription, created = SubscriptionFeeds.objects.get_or_create(link=parsed_data['link'])
        subscription.title = parsed_data['title']
        if ('image' in parsed_data and parsed_data['image']):
            subscription.image.save(
                os.path.basename(parsed_data['link']),
                File(open(result[0], 'rb'))
            )
        return subscription, created

    def parse_data(self, data):
        try:
            feed_parse = self._assert_can_parse(data)
            parse_data = self._select_fields(data, feed_parse)
        except AttributeError as error:
            raise NotParseableLinkExcepcion()
        return parse_data

    def _create_articles_for_subscription(self, subscription, parsed_data, user):
        if ('entries' in parsed_data):
            user_article_helper = UserArticleHelper()
            last_articles = parsed_data['entries'][0:(min(MAX_PERMITTED_ARTICLES, len(parsed_data['entries'])))]
            articles, new_articles_cant = user_article_helper.create_user_articles(last_articles, subscription, user)
            return articles
