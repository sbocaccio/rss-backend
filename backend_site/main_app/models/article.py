from django.db import models
from django.utils import timezone
from ..models.subscription_feed_model import SubscriptionFeeds

class Article(models.Model):
   link = models.URLField(max_length=250)
   summary = models.TextField(max_length=1000)
   title = models.TextField(max_length=250)
   image = models.ImageField(null=True, blank=True)
   subscriptions_feed = models.ManyToManyField(SubscriptionFeeds)
   created_at = models.DateTimeField(default = timezone.now())



