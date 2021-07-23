from django.db import models
from django.contrib.auth.models import User
from ..models.subscription_feed_model import SubscriptionFeeds

class Article(models.Model):
   subscription = models.ForeignKey(SubscriptionFeeds,on_delete=models.CASCADE)
   link = models.URLField(max_length=250)
   summary = models.TextField(max_length=1000)
   title = models.TextField(max_length=250)
   users_subscribed = models.ManyToManyField(User)
   date_time = models.DateTimeField(null=True)

