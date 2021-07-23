from ...models import Article
from django.utils import timezone
class ArticleHelper():
    def createArticles(self,articles,subscription,user):
        for article in articles:
            article_fields = {}
            article_fields['title'] = article['title']
            article_fields['summary'] = article['summary']
            article_fields['link'] = article['link']
            article_fields['subscription'] = subscription

            article_model, created = Article.objects.get_or_create(**article_fields)
            article_model.users_subscribed.add(user)
            article_model.date_time = timezone.now()
            article_model.save()

