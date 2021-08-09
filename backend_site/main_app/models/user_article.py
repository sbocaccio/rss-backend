from django.contrib.auth.models import User
from django.db import models


from ..models.article import Article
from ..managers.user_articles_manager import UserArticleManager


class UserArticle(models.Model):

    read = models.BooleanField(default=False)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    objects = UserArticleManager()
    class Meta:
        unique_together = ['article', 'user']
