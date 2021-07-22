from django.urls import path
from .views.register import RegisterApi
from .views.login import LoginAPIView
from .views.subscription_feed import SubscriptionFeedAPI
from .views.articles import ArticleAPI

urlpatterns = [
    path('register/', RegisterApi.as_view(), name=''),
    path('login/',LoginAPIView.as_view(),name=''),
    path('feed/', SubscriptionFeedAPI.as_view(),name='feed'),
    path('articles/',ArticleAPI.as_view(),name='feed'),
]
