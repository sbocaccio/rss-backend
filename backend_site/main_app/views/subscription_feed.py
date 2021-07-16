from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from ..models.subscription_feed_model import SubscriptionFeed
from ..serializers.suscription_feed_serializer import CreateFeedSerializers
from rest_framework.response import Response
from django.forms.models import model_to_dict
from django.forms.models import model_to_dict
import json
from django.core import serializers




class CreateSubscriptionFeedAPI(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        serializer = CreateFeedSerializers(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        feed = serializer.save()

        return Response({
            "message": "Succesfully created feed.",
            "link": feed.link,
            'title': feed.title,
            "image": feed.image,
        })


