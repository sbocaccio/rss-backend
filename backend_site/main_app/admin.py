from django.contrib import admin
from django.contrib.auth.models import User

from .models.article import Article
from .models.subscription_feed_model import SubscriptionFeeds
from .models.user_article import UserArticle


def customTitledFilter(title):
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance
    return Wrapper

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("link", "title", 'created_at', 'subscriptions_its_belongs')
    search_fields = ("link", "title")
    list_filter = (("subscriptions_feed__title", customTitledFilter('subscriptions its belongs'))
                   , "created_at")

    def subscriptions_its_belongs(self, article):
        return ", ".join(
            [str(subscription) for subscription in article.subscriptions_feed.all().values_list('title', flat=True)])



class ClassInline(admin.TabularInline):
    model = ArticleAdmin


@admin.register(SubscriptionFeeds)
class SubscriptionFeedsAdmin(admin.ModelAdmin):
    list_display = ("link", "title", 'users__subscribed')
    search_fields = ["link", "title", 'users_subscribed__username']
    list_filter = ["title", 'users_subscribed']
    inlines = [
        ClassInline,
    ]


    def users__subscribed(self, subscription):
        return ", ".join([str(user) for user in subscription.users_subscribed.all()])




@admin.register(UserArticle)
class UserArticleAdmin(admin.ModelAdmin):
    list_display = ("user", "article_title")
    search_fields = ["user__username", "article__title"]
    list_filter = ["user"]
    fields = ['foreign_key__related_id']


    def article_title(self, user_article):
        return user_article.article.title
