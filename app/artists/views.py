from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from app.core.models import ArtistProfile
from app.core.permission import IsArtist, IsArtistManager, IsSuperAdmin
from app.core.serializers import ArtistProfileSerializer
from .services import (
    get_raw_artist_profile_list_queries,
    get_raw_artist_profile_detail_queries,
    create_raw_artist_profile_queries,
    update_raw_artist_profile_queries,
    delete_raw_artist_profile_queries,
    get_raw_artist_profile_by_user_id_queries,  # Import the new function
)
from django.http import Http404
from rest_framework.permissions import IsAuthenticated


class ArtistProfileCreateView(APIView):
    """View for creating Artist Profiles."""

    permission_classes = [permissions.AllowAny]
    serializer_class = ArtistProfileSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            success, data = create_raw_artist_profile_queries(
                request.user.id, serializer.validated_data
            )
            if success:
                return Response(data, status=status.HTTP_201_CREATED)
            else:
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArtistProfileListView(APIView):
    """View for listing Artist Profiles."""

    permission_classes = [permissions.AllowAny]
    serializer_class = ArtistProfileSerializer

    def get(self, request):
        artists = get_raw_artist_profile_list_queries()
        return Response(artists)


class ArtistProfileDetailView(APIView):
    """View for retrieving, updating, or deleting an Artist Profile."""

    permission_classes = [IsArtist| IsArtistManager|IsSuperAdmin | permissions.AllowAny]
    serializer_class = ArtistProfileSerializer

    def get(self, request, pk):
        artist = get_raw_artist_profile_detail_queries(pk)
        if artist:
            return Response(artist)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            success, data = update_raw_artist_profile_queries(
                pk, serializer.validated_data
            )
            if success:
                return Response(data)
            else:
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        deleted = delete_raw_artist_profile_queries(pk)
        if deleted:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)


class ArtistProfileByUserView(APIView):
    """View for retrieving an Artist Profile by User ID."""

    permission_classes = [permissions.AllowAny]
    serializer_class = ArtistProfileSerializer

    def get(self, request, user_id):
        try:
            artist_profile = get_raw_artist_profile_by_user_id_queries(user_id)
            return Response(artist_profile, status=status.HTTP_200_OK)
        except Http404 as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(
                {"detail": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
