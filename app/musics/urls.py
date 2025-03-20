from django.urls import path
from .views import (
    MusicCreateView,
    MusicListView,
    MusicDetailView,
    # MusicAddArtistView,
)

app_name = "musics"

urlpatterns = [
    # Music Endpoints
    path("music/", MusicCreateView.as_view(), name="music-create"),
    path("music/list/", MusicListView.as_view(), name="music-list"),
    path("music/<uuid:pk>/", MusicDetailView.as_view(), name="music-detail"),
]
