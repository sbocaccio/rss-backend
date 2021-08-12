from django.contrib import admin

# Register your models here.

from .models.article import Article
from .models.subscription_feed_model import SubscriptionFeeds
from .models.user_article import UserArticle



@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):

    def custom_titled_filter(title):
        class Wrapper(admin.FieldListFilter):
            def __new__(cls, *args, **kwargs):
                instance = admin.FieldListFilter.create(*args, **kwargs)
                instance.title = title
                return instance

        return Wrapper

    list_display = ("link", "title",'subscriptions_its_belongs',"created_at")
    search_fields = ("link", "title")
    list_filter = (("subscriptions_feed__title", custom_titled_filter('subscriptions it belongs'))
                   , "created_at")

    def subscriptions_its_belongs(self, article):
        return article.subscriptions_feed.all().count()


@admin.register(SubscriptionFeeds)
class SubscriptionFeedsAdmin(admin.ModelAdmin):
    list_display = ("link", "title", 'users__subscribed')
    search_fields = ["link", "title", 'users_subscribed__username']
    list_filter = ["title", 'users_subscribed']

    def users__subscribed(self, subscription):
        return subscription.users_subscribed.all().count()

@admin.register(UserArticle)
class UserArticleAdmin(admin.ModelAdmin):
    list_display = ("user", "article_title")
    search_fields = ["user__username", "article__title"]
    list_filter = ["user"]

    def article_title(self, user_article):
        return user_article.article.title

