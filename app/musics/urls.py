from django.urls import path
from .views import (
    MusicCreateView,
    MusicListView,
    MusicDetailView,
    MusicAddArtistView,
    MusicArtistsListView,
    MusicArtistsDetailView,
)

app_name = "musics"

urlpatterns = [
    # Music Endpoints
    path("music/", MusicCreateView.as_view(), name="music-create"),
    path("music/list/", MusicListView.as_view(), name="music-list"),
    path("music/<uuid:pk>/", MusicDetailView.as_view(), name="music-detail"),
    path(
        "music/<uuid:pk>/add-artist/",
        MusicAddArtistView.as_view(),
        name="music-add-artist",
    ),
    # Music-Artist Relationship Endpoints
    path("music-artists/", MusicArtistsListView.as_view(), name="music-artists-list"),
    path(
        "music-artists/<uuid:pk>/",
        MusicArtistsDetailView.as_view(),
        name="music-artists-detail",
    ),
]
