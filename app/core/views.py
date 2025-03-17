from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.decorators import action

from .models import UserProfile, ArtistProfile, Music, MusicArtists  # Adjust import paths as needed
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    UserProfileSerializer,
    ArtistProfileSerializer,
    MusicSerializer,
    MusicArtistsSerializer
)


class RegisterView(CreateAPIView):
    """User Registration View."""
    queryset = get_user_model().objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """Viewset for User model (Read-Only)."""
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserProfileViewSet(viewsets.ModelViewSet):
    """Viewset for User Profiles."""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Restrict users to see only their own profile."""
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Set the user when creating a profile."""
        serializer.save(user=self.request.user)


class ArtistProfileViewSet(viewsets.ModelViewSet):
    """Viewset for managing artists."""
    queryset = ArtistProfile.objects.all()
    serializer_class = ArtistProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class MusicViewSet(viewsets.ModelViewSet):
    """Viewset for managing music."""
    queryset = Music.objects.all()
    serializer_class = MusicSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        """Custom create method to handle music-artist relationship."""
        music = serializer.save()
        artists = self.request.data.get("artists", [])
        if artists:
            artist_instances = ArtistProfile.objects.filter(id__in=artists)
            music.artists.set(artist_instances)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def add_artist(self, request, pk=None):
        """Custom action to add an artist to a music record."""
        music = self.get_object()
        artist_id = request.data.get("artist_id")

        if not artist_id:
            return Response({"error": "Artist ID required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            artist = ArtistProfile.objects.get(id=artist_id)
            music.artists.add(artist)
            return Response({"message": "Artist added successfully."}, status=status.HTTP_200_OK)
        except ArtistProfile.DoesNotExist:
            return Response({"error": "Artist not found."}, status=status.HTTP_404_NOT_FOUND)


class MusicArtistsViewSet(viewsets.ModelViewSet):
    """Viewset for Music-Artist relationships."""
    queryset = MusicArtists.objects.all()
    serializer_class = MusicArtistsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
