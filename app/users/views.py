# from venv import logger
from asyncio.log import logger
from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from app.core.models import ArtistProfile, Music, MusicArtists ,User

from app.core.serializers import UserProfileSerializer, UserSerializer
from .services import (
    get_all_raw_user_profiles_queries,
    get_raw_user_detail_queries,
    get_raw_user_list_queries,
    get_raw_user_profile_list_queries,
    get_raw_user_profile_detail_queries,
    create_raw_user_profile_queries,
    update_raw_user_profile_queries,
    delete_raw_user_profile_queries,
)


class UserListView(APIView):
    """View for listing users (Read-Only)."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request):
        users = get_raw_user_list_queries()
        serializer = self.serializer_class(users, many=True)
        return Response(serializer.data)


class UserDetailView(APIView):
    """View for retrieving a single user (Read-Only)."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request, pk):
        user = get_raw_user_detail_queries(pk)
        serializer = self.serializer_class(user)
        return Response(serializer.data)


class UserProfileCreateView(APIView):
    """View for creating User Profiles."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                success, data = create_raw_user_profile_queries(
                    request.user.id, serializer.validated_data
                )
                if success:
                    return Response(data, status=status.HTTP_201_CREATED)
                else:
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                # Log database errors
                logger.error(f"Error creating user profile: {e}")
                return Response({"error": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            # Return serializer errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class UserProfileListView(APIView):
    """View for listing User Profiles."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get(self, request):
        # profile=User.objects.all()
        profiles = get_raw_user_profile_list_queries(request.user.id)
        serializer = self.serializer_class(data=profiles, many=True)
        serializer.is_valid()
        return Response(serializer.data)


class UserProfileDetailView(APIView):
    """View for retrieving, updating, or deleting a User Profile."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get(self, request, pk):
        profile = get_raw_user_profile_detail_queries(request.user.id, pk)
        if profile:
            serializer = self.serializer_class(data=profile)
            serializer.is_valid()
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            success, data = update_raw_user_profile_queries(
                request.user.id, pk, serializer.validated_data
            )
            if success:
                return Response(data)
            else:
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        deleted = delete_raw_user_profile_queries(request.user.id, pk)
        if deleted:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)



class AllUserProfileListView(APIView):
    """View for listing all User Profiles."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get(self, request):
        profiles = get_all_raw_user_profiles_queries()
        serializer = self.serializer_class(data=profiles, many=True)
        serializer.is_valid()
        return Response(serializer.data)
