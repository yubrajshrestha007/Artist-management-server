from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate

from .models import UserProfile, ArtistProfile, Music, MusicArtists
from .serializers import (
    LoginSerializer,
    RegisterSerializer,
    ArtistProfileSerializer,
)

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


# class UserListView(APIView):
#     """View for listing users (Read-Only)."""

#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = UserSerializer

#     def get(self, request):
#         users = get_user_model().objects.all()
#         serializer = self.serializer_class(users, many=True)
#         return Response(serializer.data)


# class UserDetailView(APIView):
#     """View for retrieving a single user (Read-Only)."""

#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = UserSerializer

#     def get(self, request, pk):
#         user = get_object_or_404(get_user_model(), pk=pk)
#         serializer = self.serializer_class(user)
#         return Response(serializer.data)


# class UserProfileCreateView(APIView):
#     """View for creating User Profiles."""

#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = UserProfileSerializer

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class UserProfileListView(APIView):
#     """View for listing User Profiles."""

#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = UserProfileSerializer

#     def get(self, request):
#         profiles = UserProfile.objects.filter(user=request.user)
#         serializer = self.serializer_class(profiles, many=True)
#         return Response(serializer.data)


# class UserProfileDetailView(APIView):
#     """View for retrieving, updating, or deleting a User Profile."""

#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = UserProfileSerializer

#     def get(self, request, pk):
#         profile = get_object_or_404(UserProfile, pk=pk, user=request.user)
#         serializer = self.serializer_class(profile)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         profile = get_object_or_404(UserProfile, pk=pk, user=request.user)
#         serializer = self.serializer_class(profile, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         profile = get_object_or_404(UserProfile, pk=pk, user=request.user)
#         profile.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class ArtistProfileCreateView(APIView):
#     """View for creating Artist Profiles."""

#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#     serializer_class = ArtistProfileSerializer

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ArtistProfileListView(APIView):
#     """View for listing Artist Profiles."""

#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#     serializer_class = ArtistProfileSerializer

#     def get(self, request):
#         artists = ArtistProfile.objects.all()
#         serializer = self.serializer_class(artists, many=True)
#         return Response(serializer.data)


# class ArtistProfileDetailView(APIView):
#     """View for retrieving, updating, or deleting an Artist Profile."""

#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#     serializer_class = ArtistProfileSerializer

#     def get(self, request, pk):
#         artist = get_object_or_404(ArtistProfile, pk=pk)
#         serializer = self.serializer_class(artist)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         artist = get_object_or_404(ArtistProfile, pk=pk)
#         serializer = self.serializer_class(artist, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         artist = get_object_or_404(ArtistProfile, pk=pk)
#         artist.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
