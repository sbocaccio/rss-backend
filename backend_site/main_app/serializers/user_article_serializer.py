from rest_framework import serializers


from ..models.user_article import UserArticle
from .article_serializer import ArticleSerializers

class UserArticleSerializers(serializers.ModelSerializer):
    article = ArticleSerializers()
    class Meta:
        model = UserArticle
        fields = ['user', 'article','read','pk']
