from rest_framework import serializers

from .article_serializer import ArticleSerializers
from ..models.user_article import UserArticle


class UserArticleSerializers(serializers.ModelSerializer):
    article = ArticleSerializers()

    class Meta:
        model = UserArticle
        fields = ['user', 'article', 'read', 'pk']


