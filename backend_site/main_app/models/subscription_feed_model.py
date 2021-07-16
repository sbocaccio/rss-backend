from os import link
from django.db import models
from django.contrib.auth.models import User



class SubscriptionFeed(models.Model):
    link = models.CharField(max_length=250)
    title = models.CharField(max_length=250)
    users_subscribed = models.ManyToManyField(User)
    image = models.CharField(max_length=250)
