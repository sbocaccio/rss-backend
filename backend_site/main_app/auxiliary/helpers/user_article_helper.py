import urllib.request
from django.core.files import File
from django.utils import timezone

from ...models.article import Article
from ...models.user_article import UserArticle


class UserArticleHelper():

    def get_or_create_article(self, article, subscription):
        article_fields = {}
        article_fields['title'] = article['title']
        article_fields['summary'] = article['summary']
        article_fields['link'] = article['link']

        article_model, created = Article.objects.get_or_create(**article_fields)
        article_model.date_time = timezone.now()
        article_model.subscriptions_feed.add(subscription)

        if ('media_content' in article):
            try:
                result = urllib.request.urlretrieve(article['media_content'][0]['url'])
            except:
                article_model['image'] = ''

        if (article_model.image):
            subscription.image.save(
                os.path.basename(article['media_content'][0]['url']),
                File(open(result[0], 'rb'))
            )
        article_model.save()
        return article_model

    def get_or_create_user_article(self, article, user, subscription):
        user_article_fields = {}
        user_article_fields['article'] = article
        user_article_fields['user'] = user
        user_article_model, created = UserArticle.objects.get_or_create(**user_article_fields)
        user_article_model.save()

    def create_user_articles(self, articles, subscription, user):
        articles.reverse()  # Newer feeds must be the latest created.
        created_articles = []
        for article in articles:
            article = self.get_or_create_article(article, subscription)
            created_articles.append(article)
            self.get_or_create_user_article(article, user, subscription)
        return created_articles

    def sort_by_date(self, user_articles):
        user_articles_list = list(user_articles)
        user_articles_list.sort(key=lambda user_article: user_article.date_time, reverse=True)
        return user_articles_list
