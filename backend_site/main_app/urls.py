from django.urls import path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from .views.articles import ArticleAPI
from .views.login import LoginAPIView
from .views.register import RegisterApi
from .views.subscription_feed import SubscriptionFeedAPI
from rest_framework import routers

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'feed/', SubscriptionFeedAPI,basename= 'feed')

subscription_feed_delete_and_refresh = SubscriptionFeedAPI.as_view({
    'delete': 'destroy',
    'put': 'refresh',
})
urlpatterns = format_suffix_patterns([
    path('register/', RegisterApi.as_view(), name=''),
    path('login/', LoginAPIView.as_view(), name=''),
    path('subscriptions/<int:pk>/', subscription_feed_delete_and_refresh, name='delete_and_refresh'),
    path('subscriptions/<int:pk>/articles/', ArticleAPI.as_view(), name='articles'),
])

urlpatterns += router.urls