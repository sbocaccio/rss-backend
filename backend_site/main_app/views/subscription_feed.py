from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from ..models.subscription_feed_model import SubscriptionFeeds
from ..serializers.suscription_feed_serializer import CreateFeedSerializers


class SubscriptionFeedAPI(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateFeedSerializers

    def get_queryset(self):
        user = self.request.user
        user_subscriptions = SubscriptionFeeds.objects.filter(users_subscribed=user)
        return user_subscriptions


