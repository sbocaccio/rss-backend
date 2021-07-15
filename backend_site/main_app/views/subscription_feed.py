
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import SubscriptionFeed


class CreateSubscriptionFeedAPI(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = CreateFeedSerializers(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        ## ACA HABRIA QUE TRY QUE PUEDE HACERLO
        serializer.save()
        return Response({
            "message": "Succesfully created feed.",
        })        

