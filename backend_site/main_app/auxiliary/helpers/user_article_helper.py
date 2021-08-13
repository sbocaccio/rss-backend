import os
import urllib.request
from django.core.files import File
from django.db.models import Count
from ...models.article import Article
from ...models.user_article import UserArticle
from .constants import MAX_PERMITTED_ARTICLES

class UserArticleHelper():

    def get_or_create_article(self, article, subscription):
        article_model, created = Article.objects.get_or_create(link=article['link'])
        article_model.title = article['title']
        article_model.summary = article['summary']
        article_model.subscriptions_feed.add(subscription)
        self.add_image_to_article(article, article_model)

        article_model.save()
        return article_model,created

    def add_image_to_article(self, article, article_model):
        image = ''
        try:
            if ('media_content' in article):
                image = article['media_content'][0]['url']
            elif 'links' in article and 'href' in article['links'][1]:
                image = article['links'][1]['href']

            if image:
                result = urllib.request.urlretrieve(image)
                article_model.image.save(
                    os.path.basename(image),
                    File(open(result[0], 'rb')))
        except:
            article_model.image = None

    def get_or_create_user_article(self, article, user):
        user_article_fields = {}
        user_article_fields['article'] = article
        user_article_fields['user'] = user
        user_article_model, created = UserArticle.objects.get_or_create(**user_article_fields)
        user_article_model.save()
        return user_article_model,created

    def create_user_articles(self, articles, user):
        all_articles = []
        articles_created = 0
        for article in articles:
            user_article_model,created = self.get_or_create_user_article(article, user)
            if(created):
                articles_created+=1
        return all_articles,articles_created

    def delete_all_user_articles_from_subscription(self, user,articles_of_subscription):
        no_more_readable_user_article = UserArticle.objects.not_more_readable_user_articles_from_user_and_subscription(user,articles_of_subscription)
        self.delete_user_articles_from_subscription(no_more_readable_user_article)

    def delete_user_articles_from_subscription(self, user_articles_to_delete):
        '''
        This method deletes the user_articles of the user if that article it is not in other subscription the user is subscribed.
        It also deletes the articles that are not matched to any user ( this user was the last one) because they are not going to be read anymore.
        '''
        user_articles_to_delete_list = list(user_articles_to_delete)
        articles_id_of_user_articles = [user_article.article.id for user_article in user_articles_to_delete_list]
        user_articles_to_delete.delete()
        still_readable_articles_id = list(
            UserArticle.objects.user_articles_of_articles_id(articles_id_of_user_articles).values_list('article_id',
                                                                                                       flat=True))

        self._delete_not_more_readable_articles(articles_id_of_user_articles, still_readable_articles_id)

    def _delete_not_more_readable_articles(self, articles_id_of_user_articles, still_readable_articles_id):

        articles_to_delete = Article.objects.all().filter(pk__in=articles_id_of_user_articles).exclude(
            pk__in=still_readable_articles_id)
        articles_to_delete.delete()

    def remove_old_user_articles_from_subscription_and_user(self, subscription, user):
        updated_user_articles_id = UserArticle.objects.all_user_articles_from_user_and_subscription_sorted_in_ascending_date_order(
            user, subscription).values_list('id', flat=True)
        if (len(updated_user_articles_id) > MAX_PERMITTED_ARTICLES):
            user_articles_to_be_deleted_id = updated_user_articles_id[:len(updated_user_articles_id) - MAX_PERMITTED_ARTICLES]
            user_articles_to_be_deleted = UserArticle.objects.filter(id__in=user_articles_to_be_deleted_id)
            self.delete_user_articles_from_subscription(user_articles_to_be_deleted)
