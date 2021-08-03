from django.core import serializers
from http import HTTPStatus
from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..auxiliary.exceptions.not_subscribed_exception import NotSubscribedException
from ..auxiliary.helpers.user_article_helper import UserArticleHelper
from ..models.article import Article
from ..models.subscription_feed_model import SubscriptionFeeds
from ..models.user_article import UserArticle
from ..serializers.suscription_feed_serializer import CreateFeedSerializers
from ..serializers.suscription_feed_serializer import SubscriptionFeedHelper
from ..serializers.user_article_serializer import UserArticleSerializers


class SubscriptionFeedAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateFeedSerializers
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        user_subscriptions = SubscriptionFeeds.objects.filter(users_subscribed=user)
        return user_subscriptions

    def destroy(self, *args, **kwargs):
        subscription = self.check_user_is_subscribed_to_subscription(kwargs['id'], self.request.user)
        self.delete_user_articles_from_user(self.request)
        subscription.users_subscribed.remove(self.request.user)
        if (not subscription.users_subscribed.exists()):
            subscription.delete()
        return Response(
            status=HTTPStatus.NO_CONTENT
        )

    def delete_user_articles_from_user(self, request):
        user_article_helper = UserArticleHelper()
        user_article_helper.delete_all_user_articles_from_subscription(request.user)

    def check_user_is_subscribed_to_subscription(self, subscription_id, user):
        try:
            subscription = SubscriptionFeeds.objects.get(id=subscription_id, users_subscribed=user)
        except:
            raise NotSubscribedException()
        return subscription

    def refresh(self, *args, **kwargs):
        subscription = self.check_user_is_subscribed_to_subscription(kwargs['id'], self.request.user)
        subscription_helper = SubscriptionFeedHelper()
        user_articles = subscription_helper.update_subscription(subscription, self.request.user)
        data=UserArticleSerializers(instance= user_articles, many= True)
        return Response(data.data)
