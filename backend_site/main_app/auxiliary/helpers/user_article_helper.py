import os
import urllib.request
from django.core.files import File
from django.db.models import Count

from ...models.article import Article
from ...models.user_article import UserArticle


class UserArticleHelper():

    def get_or_create_article(self, article, subscription):
        article_model, created = Article.objects.get_or_create(link=article['link'])
        article_model.title = article['title']
        article_model.summary = article['summary']
        article_model.subscriptions_feed.add(subscription)

        if ('media_content' in article):
            try:
                result = urllib.request.urlretrieve(article['media_content'][0]['url'])
                article_model.image.save(
                    os.path.basename(article['media_content'][0]['url']),
                    File(open(result[0], 'rb')))
            except:
                article_model['image'] = ''

        article_model.save()
        return article_model

    def get_or_create_user_article(self, article, user):
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
            self.get_or_create_user_article(article, user)
        return created_articles

    def sort_by_date(self, user_articles):
        user_articles_list = list(user_articles)
        user_articles_list.sort(key=lambda user_article: user_article.date_time, reverse=True)
        return user_articles_list


    def delete_user_articles_from_subscription(self, user):
        user_articles_to_delete = UserArticle.objects.annotate(
            num_subscription=Count('article__subscriptions_feed')).filter(user=user, num_subscription=1)
        articles_id_of_user_articles = list(user_articles_to_delete.values_list('article_id', flat=True))
        user_articles_to_delete.delete()
        still_readable_articles_id = list(UserArticle.objects.filter(article__id__in  = articles_id_of_user_articles).values_list('article_id', flat=True))
        self._delete_not_more_readable_articles(articles_id_of_user_articles,still_readable_articles_id)

    def _delete_not_more_readable_articles(self, articles_to_delete_id,id_de_articulos_que_tienen_lectores):
        articles_to_delete = Article.objects.filter(pk__in=articles_to_delete_id).exclude(pk__in= id_de_articulos_que_tienen_lectores)
        articles_to_delete.delete()
