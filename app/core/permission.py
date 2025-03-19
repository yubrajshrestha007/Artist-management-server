from rest_framework import permissions
from .models import ROLE_CHOICES


class IsSuperAdmin(permissions.BasePermission):
    """Allows access only to super admins."""

    def has_permission(self, request, view):
        return request.user and request.user.role == ROLE_CHOICES.super_admin



class IsArtistManager(permissions.BasePermission):
    """Allows access only to artist managers."""

    def has_permission(self, request, view):
        return request.user and request.user.role == ROLE_CHOICES.artist_manager


class IsArtist(permissions.BasePermission):
    """Allows access only to artists."""

    def has_permission(self, request, view):
        return request.user and request.user.role == ROLE_CHOICES.artist


# class IsSuperAdminOrArtistManager(permissions.BasePermission):
#     """Allows access to super admins and artist managers."""

#     def has_permission(self, request, view):
#         return request.user and request.user.role in [
#             ROLE_CHOICES.super_admin,
#             ROLE_CHOICES.artist_manager,
#         ]


# class IsArtistOrReadOnly(permissions.BasePermission):
#     """Allows artists to modify, others read-only."""

#     def has_permission(self, request, view):
#         return request.method in permissions.SAFE_METHODS or (
#             request.user and request.user.role == ROLE_CHOICES.artist
#         )


# class IsSuperAdminOrReadOnly(permissions.BasePermission):
#     """Allows super admins to modify, others read-only."""

#     def has_permission(self, request, view):
#         return request.method in permissions.SAFE_METHODS or (
#             request.user and request.user.role == ROLE_CHOICES.super_admin
#         )
