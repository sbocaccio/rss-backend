from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


from ..auxiliary.helpers.user_folder_helper import UserFolderHelper


class UserFolderAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        user_folder_helper = UserFolderHelper()
        user_folder_helper.create_folder(request.data,request.user)
        return Response({
            "message": 'You Succesfully loged in',
        })
