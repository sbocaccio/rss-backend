from os import link
from django.db import models
from django.contrib.auth.models import User



class SubscriptionFeeds(models.Model):
    users_subscribed = models.ManyToManyField(User)
    link = models.CharField(max_length=250)
    title = models.CharField(max_length=250)
    image = models.ImageField(upload_to='photos')
