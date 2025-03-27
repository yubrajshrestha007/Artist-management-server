from django.urls import path
from .views import ArtistProfileCreateView, ArtistProfileListView, ArtistProfileDetailView, ArtistProfileByUserView

urlpatterns = [
    path('artists/', ArtistProfileCreateView.as_view(), name='artist-profile-create'),
    path('artists/list/', ArtistProfileListView.as_view(), name='artist-profile-list'),
    path('artists/<uuid:pk>/', ArtistProfileDetailView.as_view(), name='artist-profile-detail'),
    path('artists/by-user/<uuid:user_id>/', ArtistProfileByUserView.as_view(), name='artist-profile-by-user'),
]
