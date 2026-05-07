from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .serializers import RegisterSerializer


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]   # ✅ THIS IS THE FIX

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User created successfully",
                "user": serializer.data
            }, status=201)

        return Response(serializer.errors, status=400)