# /home/mint/Desktop/ArtistMgntBack/app/core/permission.py

from rest_framework import permissions
from .models import ArtistProfile

class IsArtist(permissions.BasePermission):
    """Check if the user is an artist."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "artist"


class IsArtistManager(permissions.BasePermission):
    """Check if the user is an artist manager."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "artist_manager"


class IsSuperAdmin(permissions.BasePermission):
    """Check if the user is a super admin."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "super_admin"

class IsMusicCreator(permissions.BasePermission):
    """
    Allows access only to the artist who created the music record.
    """

    def has_object_permission(self, request, view, obj):
        # Allow all safe methods (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Check if the user is an authenticated artist
        if request.user.is_authenticated and request.user.role == "artist":
            try:
                # Get the artist profile associated with the user
                artist_profile = ArtistProfile.objects.get(user=request.user)
                # Check if the artist created the music record
                return obj.created_by == artist_profile
            except ArtistProfile.DoesNotExist:
                return False
        return False

class IsAuthenticated(permissions.BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)
