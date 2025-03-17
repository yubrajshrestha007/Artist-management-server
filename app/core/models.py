"""
Database Models.
"""

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from model_utils.choices import Choices
from model_utils.models import TimeStampedModel, UUIDModel

from .manager import UserManager


# ==============================
# CHOICE DEFINITIONS
# ==============================

ROLE_CHOICES = Choices("artist", "artist_manager", "super_admin")
GENDER_CHOICES = Choices("male", "female", "other")
GENRE_CHOICES = Choices("rnb", "country", "classic", "rock", "jazz", "pop")


# ==============================
# UTILITY FUNCTIONS
# ==============================

def validate_date(value):
    """Ensure date is not in the future."""
    if value > timezone.now():
        raise ValidationError(_("Date must not be in the future."))


# ==============================
# USER MODEL
# ==============================

class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel, UUIDModel):
    """Custom user model."""

    email = models.EmailField(_("Email Address"), max_length=255, unique=True)
    password = models.CharField(_("Password"), max_length=255)
    is_staff = models.BooleanField(_("Is Staff?"), default=False)
    is_active = models.BooleanField(_("Is Active?"), default=True)
    date_joined = models.DateTimeField(_("Joined Date"), auto_now_add=True)
    role = models.CharField(_("Role"), max_length=20, choices=ROLE_CHOICES, default=ROLE_CHOICES.artist)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = _("User")

    def __str__(self) -> str:
        """String representation of the user."""
        return self.email

    def get_absolute_url(self) -> str:
        """Get URL for user detail view."""
        return reverse("users:detail", kwargs={"pk": self.id})


# ==============================
# PROFILE MODELS
# ==============================

class Profile(UUIDModel, TimeStampedModel):
    """Abstract base profile model."""

    date_of_birth = models.DateTimeField(_("Date of Birth"), null=True, blank=True, validators=[validate_date])
    gender = models.CharField(_("Gender"), max_length=10, choices=GENDER_CHOICES, default=GENDER_CHOICES.male)
    address = models.CharField(_("Full Address"), max_length=255, null=True, blank=True)

    class Meta:
        abstract = True


class UserProfile(Profile):
    """User profile model."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField(_("First Name"), max_length=255, null=True, blank=True)
    last_name = models.CharField(_("Last Name"), max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = _("User Profile")

    def __str__(self) -> str:
        """String representation of the profile."""
        return f"{self.first_name} {self.last_name}".strip() if self.first_name else f"Profile of {self.user.email}"


class ArtistProfile(Profile):
    """Artist profile model."""

    name = models.CharField(_("Name"), max_length=255)  # Required field
    first_release_year = models.PositiveIntegerField(_("First Release Year"), null=True, blank=True)
    no_of_albums_released = models.PositiveIntegerField(_("Number of Albums Released"), default=0)

    class Meta:
        verbose_name = _("Artist Profile")

    def __str__(self) -> str:
        """String representation of the artist."""
        return self.name


# ==============================
# MUSIC MODELS
# ==============================

class Music(UUIDModel, TimeStampedModel):
    """Music model definition."""

    title = models.CharField(_("Title"), max_length=255)  # Required field
    album_name = models.CharField(_("Album Name"), max_length=255, null=True, blank=True)
    release_date = models.DateTimeField(_("Release Date"), validators=[validate_date], null=True, blank=True)
    genre = models.CharField(_("Genre"), max_length=20, choices=GENRE_CHOICES, default=GENRE_CHOICES.rnb)
    artists = models.ManyToManyField(ArtistProfile, related_name="musics", through="MusicArtists")

    class Meta:
        verbose_name = _("Music")

    def __str__(self) -> str:
        """String representation of the music."""
        return f"{self.title} ({self.album_name})" if self.album_name else self.title

    def get_absolute_url(self) -> str:
        """Get URL for music detail view."""
        return reverse("music:detail", kwargs={"pk": self.id})


class MusicArtists(UUIDModel):
    """Intermediate model for Music and Artists relationship."""

    music = models.ForeignKey(Music, on_delete=models.CASCADE, related_name="music_artist_relations")
    artist = models.ForeignKey(ArtistProfile, on_delete=models.CASCADE, related_name="artist_music_relations")

    class Meta:
        db_table = "core_music_artists"
        verbose_name = _("Music Artist")
        verbose_name_plural = _("Music Artists")

    def __str__(self) -> str:
        """String representation of the relation."""
        return f"{self.artist.name} - {self.music.title}"
