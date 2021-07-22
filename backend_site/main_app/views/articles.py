from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from ..models.article import Article
from ..serializers.article_serializer import ArticleSerializers

from rest_framework.response import Response
from rest_framework import status
from ..models.subscription_feed_model import SubscriptionFeeds
from ..auxiliary.exceptions.not_subscribed_exception import NotSubscribedException
class ArticleAPI(ListAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = ArticleSerializers

    def get_queryset(self):
        user = self.request.user
        link = self.request.GET.get('link')
        subscriptions = SubscriptionFeeds.objects.filter(link=link, users_subscribed=user)
        if not subscriptions:
            raise NotSubscribedException()
        user_subscriptions = Article.objects.filter(users_subscribed=user , subscription= subscriptions[0])
        return user_subscriptions