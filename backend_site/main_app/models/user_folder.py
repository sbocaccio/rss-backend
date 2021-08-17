from django.contrib.auth.models import User
from django.db import models

from ..models.subscription_feed_model import SubscriptionFeeds


class UserFolder(models.Model):
    name = models.TextField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscriptions_feed = models.ManyToManyField(SubscriptionFeeds,blank=True)
