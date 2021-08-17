from http import HTTPStatus
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets

from ..auxiliary.helpers.user_folder_helper import UserFolderHelper
from ..serializers.user_folder_serializer import UserFolderSerializers


class UserFolderAPIView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserFolderSerializers

