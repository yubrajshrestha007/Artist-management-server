from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView,
    UserViewSet,
    UserProfileViewSet,
    ArtistProfileViewSet,
    MusicViewSet,
    MusicArtistsViewSet,
)

# DRF Router for ViewSets
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'user-profiles', UserProfileViewSet, basename='user-profile')
router.register(r'artists', ArtistProfileViewSet, basename='artist-profile')
router.register(r'music', MusicViewSet, basename='music')
router.register(r'music-artists', MusicArtistsViewSet, basename='music-artists')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),  # User Registration
    path('', include(router.urls)),  # Include ViewSet routes
]
