# /home/mint/Desktop/ArtistMgntBack/app/musics/views.py

from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from app.core.models import ArtistProfile, Music
from app.core.permission import IsArtist, IsSuperAdmin, IsMusicCreator
from app.core.serializers import MusicSerializer
from .services import (
    get_raw_music_list_queries,
    get_raw_music_detail_queries,
    create_raw_music_queries,
    update_raw_music_queries,
    delete_raw_music_queries,
)


class MusicCreateView(APIView):
    """View for creating Music records."""

    permission_classes = [IsArtist]  # Only artists can create music
    serializer_class = MusicSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                if request.user.role != "artist":
                    return Response({"error": "Only artists can create music."}, status=status.HTTP_403_FORBIDDEN)

                artist_profile = ArtistProfile.objects.get(user=request.user)
                success, data = create_raw_music_queries(serializer.validated_data, artist_profile.id) #pass the user_id
                if success:
                    return Response(data, status=status.HTTP_201_CREATED)
                else:
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)
            except ArtistProfile.DoesNotExist:
                return Response({"error": "Artist profile not found."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MusicListView(APIView):
    """View for listing Music records."""

    permission_classes = [IsArtist |permissions.AllowAny] # Only artists can list music
    serializer_class = MusicSerializer

    def get(self, request):
        musics = get_raw_music_list_queries()
        return Response(musics)


class MusicDetailView(APIView):
    """View for retrieving, updating, or deleting a Music record."""

    permission_classes = [IsMusicCreator]  # Apply IsMusicCreator here
    serializer_class = MusicSerializer

    def get(self, request, pk):
        music = get_raw_music_detail_queries(pk)
        if music:
            return Response(music)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            music_object = Music.objects.get(id=pk)
            self.check_object_permissions(request, music_object)  # Check permissions here
            success, data = update_raw_music_queries(pk, request.data)
            if success:
                return Response(data)
            else:
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        except Music.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"error": "An error occurred during music update."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        try:
            music_object = Music.objects.get(id=pk)
            self.check_object_permissions(request, music_object)  # Check permissions here
            deleted = delete_raw_music_queries(pk)
            if deleted:
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"error": "Music not found."}, status=status.HTTP_404_NOT_FOUND)
        except Music.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"error": "An error occurred during music delete."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
