from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response

from ..models.article import Article


class ArticleSerializers(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['link', 'title', 'summary', 'id']
