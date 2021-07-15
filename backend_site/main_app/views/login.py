from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers.login_serializer import LoginSerializers
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny




class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializers(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        update_last_login(None, user)
        refresh_token = RefreshToken.for_user(user)

        return Response({
            "message": 'You Succesfully loged in',
            'refresh': str(refresh_token),
            'access': str(refresh_token.access_token),
        })

