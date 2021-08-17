from django.urls import path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from .views.articles import ArticleAPI
from .views.login import LoginAPIView
from .views.register import RegisterApi
from .views.subscription_feed import SubscriptionFeedAPI
from .views.user_folder import UserFolderAPIView

from rest_framework import routers

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'feed/', SubscriptionFeedAPI,basename= 'feed')
router.register(r'folder',UserFolderAPIView,basename ='folder')
subscription_feed_delete_and_refresh = SubscriptionFeedAPI.as_view({
    'delete': 'destroy',
    'put': 'refresh',
})
user_articles = ArticleAPI.as_view({
    'get': 'list',
})
user_article_update_read = ArticleAPI.as_view({
    'put': 'update',
})
user_folder = UserFolderAPIView.as_view({
    'post':'create'
})

urlpatterns = format_suffix_patterns([
    path('register/', RegisterApi.as_view(), name=''),
    path('login/', LoginAPIView.as_view(), name=''),
    path('subscriptions/<int:pk>/', subscription_feed_delete_and_refresh, name='delete_and_refresh'),
    path('subscriptions/<int:pk>/articles/', user_articles, name='articles'),
    path('articles/<int:pk>/', user_article_update_read , name='update_read'),
  # path('folder/', user_folder, name='folder'),

])

urlpatterns += router.urls
a =4