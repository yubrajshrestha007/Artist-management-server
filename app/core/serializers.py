# /home/mint/Desktop/ArtistMgntBack/app/core/serializers.py

from asyncio.log import logger
from django.contrib.auth import get_user_model
from rest_framework import serializers

from app.core.validator import validate_login_credentials, validate_password_match
from .models import GENRE_CHOICES, UserProfile, ArtistProfile, Music  # Adjust import paths as needed
from .models import ROLE_CHOICES,GENDER_CHOICES


class UserSerializer(serializers.Serializer):
    """Serializer for the User model."""
    id = serializers.UUIDField(read_only=True)
    email = serializers.EmailField()
    is_staff = serializers.BooleanField()
    is_active = serializers.BooleanField()
    date_joined = serializers.DateTimeField(read_only=True)
    role = serializers.ChoiceField(choices=ROLE_CHOICES)



class RegisterSerializer(serializers.Serializer):
    """Serializer for user registration."""

    id = serializers.UUIDField(read_only=True)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8, style={"input_type": "password"})
    confirm_password = serializers.CharField(write_only=True, min_length=8, style={"input_type": "password"})
    role = serializers.ChoiceField(choices=ROLE_CHOICES)

    def validate(self, attrs):
        return validate_password_match(attrs)


class UserProfileSerializer(serializers.Serializer):
    """Serializer for user profiles, linked to the User model."""
    id = serializers.UUIDField(read_only=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    gender = serializers.ChoiceField(choices=GENDER_CHOICES, required=False,)
    date_of_birth = serializers.DateField(required=False, allow_null=True)
    address = serializers.CharField(required=False, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True)

class ArtistProfileSerializer(serializers.Serializer):
    """Serializer for artist profiles."""
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField()
    date_of_birth = serializers.DateField(required=False, allow_null=True)
    gender = serializers.ChoiceField(choices=GENDER_CHOICES, required=False,)
    address = serializers.CharField(required=False, allow_blank=True)
    first_release_year = serializers.IntegerField(required=False, allow_null=True)
    no_of_albums_released = serializers.IntegerField(default=0)

class ArtistProfileNameSerializer(serializers.Serializer):
    """Serializer for displaying artist name and ID."""
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField()


class MusicSerializer(serializers.Serializer):
    """Serializer for music records."""

    id = serializers.UUIDField(read_only=True)
    title = serializers.CharField()
    album_name = serializers.CharField(required=False, allow_blank=True)
    release_date = serializers.DateTimeField(required=False, allow_null=True)
    genre = serializers.ChoiceField(choices=GENRE_CHOICES, required=False)
    artist_info = serializers.SerializerMethodField()

    def get_artist_info(self, obj):
        """Get artist information."""
        created_by_id = obj.get("created_by_id")
        if created_by_id:
            try:
                artist = ArtistProfile.objects.get(id=created_by_id)
                serializer = ArtistProfileNameSerializer(artist)
                return serializer.data
            except ArtistProfile.DoesNotExist:
                return None
        return None


class LoginSerializer(serializers.Serializer):
    """Serializer for user login."""

    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"}, trim_whitespace=False
    )

    def validate(self, attrs):
      return validate_login_credentials(attrs)
