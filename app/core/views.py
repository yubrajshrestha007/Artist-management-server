from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.users.services import get_raw_login_queries , get_raw_register_queries # Import connection

from .serializers import LoginSerializer, RegisterSerializer
from .utils import generate_access_token, generate_refresh_token


class LoginView(APIView):
    """User Login View."""

    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]

            # Use get_raw_login_queries to get the user
            user = get_raw_login_queries(email, password)

            if user is not None:
                if not user.is_active:
                    return Response(
                        {"error": "User account is inactive."},
                        status=status.HTTP_401_UNAUTHORIZED, # Or HTTP_403_FORBIDDEN
                    )
                request.user=user
                access = generate_access_token(user)
                refresh = generate_refresh_token(user)
                return Response(
                    {
                        "access": access,
                        "refresh": refresh,
                        "user_id": str(user.id),
                        "email": user.email,
                        "role": user.role,
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
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            role = serializer.validated_data["role"]

            success, errors = get_raw_register_queries(email, password, role)

            if success:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
