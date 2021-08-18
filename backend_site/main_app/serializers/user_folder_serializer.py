from rest_framework import serializers

from ..models.user_folder import UserFolder
from ..auxiliary.helpers.user_folder_helper import UserFolderHelper


class UserFolderSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserFolder
        fields = ['name','pk', 'subscriptions_feed']


    def create(self, request, *args, **kwargs):
        user_folder_helper = UserFolderHelper()
        user_folder = user_folder_helper.create_folder(request['name'], self.context['request'].user)
        return user_folder


