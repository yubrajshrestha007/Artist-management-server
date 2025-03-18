from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import UserProfile, ArtistProfile, Music, MusicArtists  # Adjust import paths as needed
from django.contrib.auth import authenticate


class UserSerializer(serializers.Serializer):
    """Serializer for the User model."""
    id = serializers.UUIDField(read_only=True)
    email = serializers.EmailField()
    is_staff = serializers.BooleanField()
    is_active = serializers.BooleanField()
    date_joined = serializers.DateTimeField(read_only=True)
    role = serializers.CharField()

    def create(self, validated_data):
        return get_user_model().objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.role = validated_data.get('role', instance.role)
        instance.save()
        return instance


class RegisterSerializer(serializers.Serializer):
    """Serializer for user registration."""

    id = serializers.UUIDField(read_only=True)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8, style={"input_type": "password"})
    role = serializers.CharField()

    def create(self, validated_data):
        """Create a new user with encrypted password."""
        user = get_user_model().objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.Serializer):
    """Serializer for user profiles, linked to the User model."""

    id = serializers.UUIDField(read_only=True)
    user = UserSerializer(read_only=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    gender = serializers.CharField()
    date_of_birth = serializers.DateTimeField(required=False, allow_null=True)
    address = serializers.CharField(required=False, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True)

    def create(self, validated_data):
        return UserProfile.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.address = validated_data.get('address', instance.address)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.save()
        return instance


class ArtistProfileSerializer(serializers.Serializer):
    """Serializer for artist profiles."""
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField()
    first_release_year = serializers.IntegerField(required=False, allow_null=True)
    no_of_albums_released = serializers.IntegerField(default=0)

    def create(self, validated_data):
        return ArtistProfile.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.first_release_year = validated_data.get('first_release_year', instance.first_release_year)
        instance.no_of_albums_released = validated_data.get('no_of_albums_released', instance.no_of_albums_released)
        instance.save()
        return instance


class MusicSerializer(serializers.Serializer):
    """Serializer for music records."""

    id = serializers.UUIDField(read_only=True)
    title = serializers.CharField()
    album_name = serializers.CharField(required=False, allow_blank=True)
    release_date = serializers.DateTimeField(required=False, allow_null=True)
    genre = serializers.CharField()
    artists = ArtistProfileSerializer(many=True, read_only=True)

    def create(self, validated_data):
        """Override create method to handle many-to-many relationship."""
        music = Music.objects.create(**validated_data)
        return music

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.album_name = validated_data.get('album_name', instance.album_name)
        instance.release_date = validated_data.get('release_date', instance.release_date)
        instance.genre = validated_data.get('genre', instance.genre)
        instance.save()
        return instance


class MusicArtistsSerializer(serializers.Serializer):
    """Serializer for music-artist relationship."""

    id = serializers.UUIDField(read_only=True)
    music = MusicSerializer(read_only=True)
    artistProfile = ArtistProfileSerializer(read_only=True)

    def create(self, validated_data):
        return MusicArtists.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.music = validated_data.get('music', instance.music)
        instance.artist = validated_data.get('artistProfile', instance.artist)
        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    """Serializer for user login."""

    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"}, trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if not email or not password:
            raise serializers.ValidationError(
                {"error": "Email and password are required fields."}
            )

        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError({"error": "Invalid credentials."})

        attrs['user'] = user # Adding the user to the attrs
        return attrs
