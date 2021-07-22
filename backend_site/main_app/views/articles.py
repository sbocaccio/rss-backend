from django.http import HttpResponse
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from ..models.article import Article
from ..serializers.article_serializer import ArticleSerializers
from ..models.subscription_feed_model import SubscriptionFeeds
from ..auxiliary.exceptions.not_subscribed_exception import NotSubscribedException
from rest_framework import  serializers

class ArticleAPI(ListAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = ArticleSerializers

    def get_queryset(self,):

        user = self.request.user
        id = self.kwargs['id']
        subscriptions = SubscriptionFeeds.objects.filter(id=id, users_subscribed = user)
        if not subscriptions:
            raise NotSubscribedException()
        user_subscriptions = Article.objects.filter(users_subscribed=user , subscription= subscriptions[0])
        return user_subscriptions