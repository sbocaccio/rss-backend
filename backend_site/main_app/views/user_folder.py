from http import HTTPStatus
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..auxiliary.exceptions.not_subscribed_exception import NotSubscribedException
from ..auxiliary.exceptions.not_valid_user_folder import NotValidUserFolder
from ..auxiliary.helpers.user_folder_helper import UserFolderHelper
from ..models.subscription_feed_model import SubscriptionFeeds
from ..models.user_folder import UserFolder
from ..serializers.user_folder_serializer import UserFolderSerializers


class UserFolderAPIView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserFolderSerializers

    def get_queryset(self):
        return UserFolder.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        try:
            user_folder = UserFolder.objects.get(pk=kwargs['pk'], user=request.user)
            subscription = SubscriptionFeeds.objects.get(id=request.data['subscription_id'])
            user_folder.subscriptions_feed.add(subscription)
            user_folder.save()
            return Response()
        except UserFolder.DoesNotExist:
            raise NotValidUserFolder()
        except SubscriptionFeeds.DoesNotExist:
            raise NotSubscribedException()
