from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions,status
from rest_framework.response import Response


from app.core.models import ArtistProfile, Music, MusicArtists
from app.core.serializers import MusicArtistsSerializer, MusicSerializer# Create your views here.
class MusicCreateView(APIView):
    """View for creating Music records."""

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = MusicSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            music = serializer.save()
            artists_data = request.data.get("artists", [])
            if artists_data:
                artist_instances = ArtistProfile.objects.filter(id__in=artists_data)
                music.artists.set(artist_instances)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MusicListView(APIView):
    """View for listing Music records."""

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = MusicSerializer

    def get(self, request):
        music = Music.objects.all()
        serializer = self.serializer_class(music, many=True)
        return Response(serializer.data)


class MusicDetailView(APIView):
    """View for retrieving, updating, or deleting a Music record."""

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = MusicSerializer

    def get(self, request, pk):
        music = get_object_or_404(Music, pk=pk)
        serializer = self.serializer_class(music)
        return Response(serializer.data)

    def put(self, request, pk):
        music = get_object_or_404(Music, pk=pk)
        serializer = self.serializer_class(music, data=request.data)
        if serializer.is_valid():
            serializer.save()
            artists_data = request.data.get("artists", [])
            if artists_data:
                artist_instances = ArtistProfile.objects.filter(id__in=artists_data)
                music.artists.set(artist_instances)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        music = get_object_or_404(Music, pk=pk)
        music.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MusicAddArtistView(APIView):
    """View for adding an artist to a music record."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        music = get_object_or_404(Music, pk=pk)
        artist_id = request.data.get("artist_id")

        if not artist_id:
            return Response({"error": "Artist ID required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            artist = ArtistProfile.objects.get(id=artist_id)
            music.artists.add(artist)
            return Response({"message": "Artist added successfully."}, status=status.HTTP_200_OK)
        except ArtistProfile.DoesNotExist:
            return Response({"error": "Artist not found."}, status=status.HTTP_404_NOT_FOUND)


class MusicArtistsListView(APIView):
    """View for listing Music-Artist relationships."""

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = MusicArtistsSerializer

    def get(self, request):
        music_artists = MusicArtists.objects.all()
        serializer = self.serializer_class(music_artists, many=True)
        return Response(serializer.data)


class MusicArtistsDetailView(APIView):
    """View for retrieving, updating, or deleting a Music-Artist relationship."""

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = MusicArtistsSerializer

    def get(self, request, pk):
        music_artist = get_object_or_404(MusicArtists, pk=pk)
        serializer = self.serializer_class(music_artist)
        return Response(serializer.data)

    def delete(self, request, pk):
        music_artist = get_object_or_404(MusicArtists, pk=pk)
        music_artist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
