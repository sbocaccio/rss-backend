from os import link
from django.db import models



class SubscriptionFeed(models.Model):
    link = models.CharField(max_length=250)
    title = models.CharField(max_length=250)
    summary = models.CharField(max_length=500)
    user_id = models.PositiveIntegerField(default=0)
