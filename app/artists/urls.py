from django.urls import path
from .views import (
    ArtistProfileCreateView,
    ArtistProfileListView,
    ArtistProfileDetailView,
)

app_name = "artists"

urlpatterns = [
    path("artists/", ArtistProfileCreateView.as_view(), name="artist-create"),
    path("artists/list/", ArtistProfileListView.as_view(), name="artist-list"),
    path(
        "artists/<uuid:pk>/",
        ArtistProfileDetailView.as_view(),
        name="artist-detail",
    ),
]
