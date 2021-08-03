from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views.articles import ArticleAPI
from .views.login import LoginAPIView
from .views.register import RegisterApi
from .views.subscription_feed import SubscriptionFeedAPI

subscription_feed_delete_and_refresh = SubscriptionFeedAPI.as_view({
    'delete': 'destroy',
    'put': 'refresh',
})
subscription_feed_retrieve = SubscriptionFeedAPI.as_view({
    'get': 'list',
    'post': 'create',
})


urlpatterns = format_suffix_patterns([
    path('register/', RegisterApi.as_view(), name=''),
    path('login/', LoginAPIView.as_view(), name=''),
    path('feed/', subscription_feed_retrieve, name='feed'),
    path('subscriptions/<int:id>/', subscription_feed_delete_and_refresh, name='delete_and_refresh'),
    path('subscriptions/<int:id>/articles/', ArticleAPI.as_view(), name='articles'),
])
