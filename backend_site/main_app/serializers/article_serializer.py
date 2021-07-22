
from rest_framework import  serializers
from ..models.article import Article

from rest_framework.response import Response
from rest_framework import status


class ArticleSerializers(serializers.Serializer):
    link = serializers.URLField(max_length=255)
    summary = serializers.CharField(max_length=1000)
    title = serializers.CharField(max_length=250)
    date_time= serializers.DateTimeField()
    id = serializers.IntegerField()
    class Meta:
        model = Article
        fields = ['link','title','summary','id','date_time']

