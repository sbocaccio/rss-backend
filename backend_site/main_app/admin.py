from django.contrib import admin
from django.contrib.auth.models import User

from .models.article import Article
from .models.subscription_feed_model import SubscriptionFeeds
from .models.user_article import UserArticle
from .auxiliary.helpers.admin_helper import customTitledFilter




@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("link", "title", 'created_at', 'subscriptions_its_belongs')
    search_fields = ("link", "title")
    list_filter = (("subscriptions_feed__title", customTitledFilter('subscriptions its belongs'))
                   , "created_at")

    def subscriptions_its_belongs(self, article):
        return ", ".join(
            [str(subscription) for subscription in article.subscriptions_feed.all().values_list('title', flat=True)])


@admin.register(SubscriptionFeeds)
class SubscriptionFeedsAdmin(admin.ModelAdmin):
    list_display = ("link", "title", 'users__subscribed')
    search_fields = ["link", "title", 'users_subscribed__username']
    list_filter = ["title", 'users_subscribed']

    def users__subscribed(self, subscription):
        return ", ".join([str(user) for user in subscription.users_subscribed.all()])


@admin.register(UserArticle)
class UserArticleAdmin(admin.ModelAdmin):
    list_display = ("user", "article")
    search_fields = ["user__username", "article__title"]
    list_filter = ["user"]

    def article_title(self, user_article):
        return user_article.article.title
