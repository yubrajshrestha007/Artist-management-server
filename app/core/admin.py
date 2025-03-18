from django.contrib import admin
from .models import User, UserProfile, ArtistProfile, Music, MusicArtists


admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(ArtistProfile)
admin.site.register(Music)
admin.site.register(MusicArtists)
