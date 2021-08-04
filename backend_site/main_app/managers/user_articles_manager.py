from django.db import models
from django.db.models import Count

class UserArticleManager(models.Manager):
    def not_more_readable_user_articles_from_user_and_subscription(self,user,articles_of_subscription):
        return self.annotate(
            num_subscription=Count('article__subscriptions_feed')).filter(user=user, num_subscription=1,article__in= articles_of_subscription)

    def all_user_articles_sorted_by_order_from_user_and_subscription(self,user,subscription):
        return self.filter(article__in=list(subscription.subscription_articles.all()),
                                                           user=user).order_by('article__created_at').values_list('id',
                                                                                                                  flat=True)