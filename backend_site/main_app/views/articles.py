from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..auxiliary.exceptions.not_subscribed_exception import NotSubscribedException
from ..auxiliary.exceptions.not_valid_user_article import NotValidUserArticle
from ..models.article import Article
from ..models.subscription_feed_model import SubscriptionFeeds
from ..models.user_article import UserArticle
from ..serializers.user_article_serializer import UserArticleSerializers


class ArticleAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserArticleSerializers
    http_method_names= ['get','put']

    def get_queryset(self):
        user = self.request.user
        subscription_id = self.kwargs['pk']
        try:
            subscription = SubscriptionFeeds.objects.get(id=subscription_id, users_subscribed=user)
        except SubscriptionFeeds.DoesNotExist:
            raise NotSubscribedException()
        user_articles = UserArticle.objects.all_user_articles_from_user_and_subscription_sorted_in_descending_date_order(
            user, subscription)

        return user_articles

    def update(self, *args, **kwargs):
        try:
            user_article = UserArticle.objects.get(pk=self.kwargs['pk'], user=self.request.user)
            user_article.read = self.request.data['read']
            user_article.save()
            return Response()
        except UserArticle.DoesNotExist:
            raise NotValidUserArticle()
