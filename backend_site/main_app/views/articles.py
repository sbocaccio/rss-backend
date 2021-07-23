from django.http import HttpResponse
from rest_framework import serializers
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from ..auxiliary.exceptions.not_subscribed_exception import NotSubscribedException
from ..models.article import Article
from ..models.subscription_feed_model import SubscriptionFeeds
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
        articles = Article.objects.filter(users_subscribed=user, subscription=subscription)
        return articles
