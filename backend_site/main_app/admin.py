from django.contrib import admin

from .models.article import Article
from .models.subscription_feed_model import SubscriptionFeeds
from .models.user_article import UserArticle
from django.contrib.auth.models import User


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("link", "title",'created_at','get_subscriptions_feed')
    search_fields = ("link","title")
    list_filter = ("subscriptions_feed__title","created_at")

    def get_subscriptions_feed(self, article):
        return ", ".join([str(subscription) for subscription in article.subscriptions_feed.all().values_list('title',flat=True)])

@admin.register(SubscriptionFeeds)
class SubscriptionFeedsAdmin(admin.ModelAdmin):
    list_display = ("link", "title",'get_users_subscribed')
    search_fields = ["link", "title",'users_subscribed__username']
    list_filter = ["title",'users_subscribed']

    def get_users_subscribed(self, subscription):
        return ", ".join(  [str(user) for user in subscription.users_subscribed.all()])

@admin.register(UserArticle)
class UserArticleAdmin(admin.ModelAdmin):
    list_display = ("user", "article_title")
    search_fields = ["user__username","article__title"]
    list_filter = ["user"]

    def article_title(self,user_article):
        return user_article.article.title

