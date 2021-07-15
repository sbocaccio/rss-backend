from django.db import models



class SubscriptionFeed(models.Model):
    url = models.CharField(max_length=100)
    
