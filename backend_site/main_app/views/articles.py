
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from ..auxiliary.exceptions.not_subscribed_exception import NotSubscribedException

from ..models.article import Article
from ..models.subscription_feed_model import SubscriptionFeeds
from ..models.user_article import UserArticle
from ..serializers.user_article_serializer import UserArticleSerializers


class ArticleAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserArticleSerializers

    class Meta:
        model = Article
        fields = ('id', 'title', 'summary', 'link', 'image')

    def get_queryset(self):

        user = self.request.user
        subscription_id = self.kwargs['pk']
        try:
            subscription = SubscriptionFeeds.objects.get(id=subscription_id, users_subscribed=user)
        except:
            raise NotSubscribedException()
        user_articles = UserArticle.objects.all_user_articles_from_user_and_subscription_sorted_descending_date_order(user,subscription)
        return user_articles

