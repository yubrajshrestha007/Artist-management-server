from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import UserProfile, ArtistProfile, Music, MusicArtists  # Adjust import paths as needed


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model."""

    class Meta:
        model = get_user_model()
        fields = ["id", "email", "is_staff", "is_active", "date_joined"]
        read_only_fields = ["id", "date_joined"]


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""

    password = serializers.CharField(write_only=True, min_length=8, style={"input_type": "password"})

    class Meta:
        model = get_user_model()
        fields = ["id", "email", "password"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        """Create a new user with encrypted password."""
        user = get_user_model().objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profiles, linked to the User model."""

    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ["id", "user", "first_name", "last_name", "gender", "date_of_birth", "address", "phone"]
        read_only_fields = ["id"]


class ArtistProfileSerializer(serializers.ModelSerializer):
    """Serializer for artist profiles."""

    class Meta:
        model = ArtistProfile
        fields = ["id", "name", "first_release_year", "no_of_albums_released"]
        read_only_fields = ["id"]


class MusicSerializer(serializers.ModelSerializer):
    """Serializer for music records."""

    artists = ArtistProfileSerializer(many=True, read_only=True)

    class Meta:
        model = Music
        fields = ["id", "title", "album_name", "release_date", "genre", "artists"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        """Override create method to handle many-to-many relationship."""
        artists_data = validated_data.pop("artists", [])
        music = Music.objects.create(**validated_data)
        music.artists.set(artists_data)
        return music


class MusicArtistsSerializer(serializers.ModelSerializer):
    """Serializer for music-artist relationship."""

    music = MusicSerializer(read_only=True)
    artistprofile = ArtistProfileSerializer(read_only=True)

    class Meta:
        model = MusicArtists
        fields = ["id", "music", "artistprofile"]
        read_only_fields = ["id"]
