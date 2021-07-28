from django.urls import path

from .views.articles import ArticleAPI
from .views.login import LoginAPIView
from .views.register import RegisterApi
from .views.subscription_feed import SubscriptionFeedAPI

urlpatterns = [
    path('register/', RegisterApi.as_view(), name=''),
    path('login/', LoginAPIView.as_view(), name=''),
    path('feed/', SubscriptionFeedAPI.as_view(), name='feed'),
    path('subscriptions/<int:id>/articles/', ArticleAPI.as_view(), name='articles'),
]
