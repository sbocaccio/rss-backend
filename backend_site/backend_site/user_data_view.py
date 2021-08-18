from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

class UserData(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        response = {
            'username': request.user.username,
        }
        return Response(response)

