from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate

from .serializers import (
    LoginSerializer,
    RegisterSerializer)

from .utils import generate_access_token,generate_refresh_token


class LoginView(APIView):
    """User Login View."""

    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]

            user = authenticate(request, email=email, password=password)

            if user is not None:
                access = generate_access_token(user)
                refresh = generate_refresh_token(user)
                return Response(
                    {
                        "access": access,
                        "refresh": refresh,
                        "user_id": str(user.id),
                        "email": user.email,
                        'role':user.role
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "Invalid credentials"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(APIView):
    """User Registration View."""

    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
