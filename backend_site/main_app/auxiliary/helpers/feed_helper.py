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
        articles = self.create_articles_for_subscription(subscription, parsed_data)

        if articles:
            subscription.subscription_articles.add(*articles)
        user_article_helper = UserArticleHelper()
        user_articles_created,new_articles_cant = self.create_user_articles_for_articles_and_user(articles, user)
        user_article_helper.remove_old_user_articles_from_subscription_and_user(subscription, user)
        updated_articles = UserArticle.objects.all_user_articles_from_user_and_subscription_sorted_in_descending_date_order(
            user, subscription)
        return updated_articles, new_articles_cant

    def create_feed(self, subscription):
        subscription_parsed_data = self.parse_data(subscription)
        subscription = self._get_or_create_subscription_model(subscription_parsed_data)[0]
        return subscription

    def add_many_users_to_subscription(self,subscription,users):
        parsed_data = self.parse_data(subscription)
        articles = self.create_articles_for_subscription(subscription, parsed_data)
        added_users = []
        not_added_users = []
        for user in users:
            if user in subscription.users_subscribed.all():
                not_added_users.append((user, UserAlreadySubscribedException()))
            else:
                subscription.users_subscribed.add(user)
                user_article_helper = UserArticleHelper()
                user_article_helper.create_user_articles(articles, user)
                added_users.append(user)
        subscription.save()
        return added_users, not_added_users


    def add_user_to_subscription(self, subscription, user, subscription_parsed_data):
        if user in subscription.users_subscribed.all():
            raise UserAlreadySubscribedException()

        subscription.users_subscribed.add(user)
        articles = self.create_articles_for_subscription(subscription, subscription_parsed_data,)
        if articles:
            subscription.subscription_articles.add(*articles)
        subscription.save()

        return self.create_user_articles_for_articles_and_user(articles, user)

    def create_user_articles_for_articles_and_user(self, articles, user):
        user_article_helper = UserArticleHelper()
        user_articles, cant_new_articles = user_article_helper.create_user_articles(articles, user)
        return user_articles, cant_new_articles

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

    def create_articles_for_subscription(self, subscription, parsed_data):
        articles = []
        if ('entries' in parsed_data):
            user_article_helper = UserArticleHelper()
            last_articles = parsed_data['entries'][0:(min(MAX_PERMITTED_ARTICLES, len(parsed_data['entries'])))]
            last_articles.reverse() # Newer articles must have newer creation time
            for article in last_articles:
                article, created = user_article_helper.get_or_create_article(article, subscription)
                articles.append(article)
        return articles