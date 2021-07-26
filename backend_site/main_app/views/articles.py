
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

    def get_queryset(self, ):

        user = self.request.user
        subscription_id = self.kwargs['id']
        try:
            SubscriptionFeeds.objects.get(id=subscription_id, users_subscribed=user)
        except:
            raise NotSubscribedException()
        user_articles = UserArticle.objects.filter(article__subscriptions_feed__id=subscription_id, user=user)
        return user_articles

    def retrieve_articles_from_user_articles(self, user_articles):
        articles = set()
        for user_article in user_articles:
            articles.add(user_article.article)
        return articles

