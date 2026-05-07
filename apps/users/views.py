from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User created successfully",
                "user": serializer.data
            })

        return Response(serializer.errors, status=400)