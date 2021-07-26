from django.http import HttpResponse
from rest_framework import serializers
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from ..auxiliary.exceptions.not_subscribed_exception import NotSubscribedException
from ..auxiliary.helpers.user_article_helper import UserArticleHelper
from ..models.article import Article
from ..models.subscription_feed_model import SubscriptionFeeds
from ..models.user_article import UserArticle
from ..serializers.article_serializer import ArticleSerializers


class ArticleAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ArticleSerializers

    def get_queryset(self, ):

        user = self.request.user
        subscription_id = self.kwargs['id']
        try:
            subscription = SubscriptionFeeds.objects.get(id=subscription_id, users_subscribed=user)
        except:
            raise NotSubscribedException()
        user_articles = UserArticle.objects.filter(article__subscriptions_feed__id=subscription_id, user=user)
        return self.retrieve_articles_from_user_articles(user_articles)

    def retrieve_articles_from_user_articles(self, user_articles):
        articles = set()
        for user_article in user_articles:
            articles.add(user_article.article)
        return articles

