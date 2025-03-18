from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework import permissions,status
from rest_framework.response import Response
from app.core.models import ArtistProfile
from app.core.serializers import ArtistProfileSerializer

# Create your views here.
class ArtistProfileCreateView(APIView):
    """View for creating Artist Profiles."""

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ArtistProfileSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArtistProfileListView(APIView):
    """View for listing Artist Profiles."""

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ArtistProfileSerializer

    def get(self, request):
        artists = ArtistProfile.objects.all()
        serializer = self.serializer_class(artists, many=True)
        return Response(serializer.data)


class ArtistProfileDetailView(APIView):
    """View for retrieving, updating, or deleting an Artist Profile."""

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ArtistProfileSerializer

    def get(self, request, pk):
        artist = get_object_or_404(ArtistProfile, pk=pk)
        serializer = self.serializer_class(artist)
        return Response(serializer.data)

    def put(self, request, pk):
        artist = get_object_or_404(ArtistProfile, pk=pk)
        serializer = self.serializer_class(artist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        artist = get_object_or_404(ArtistProfile, pk=pk)
        artist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
