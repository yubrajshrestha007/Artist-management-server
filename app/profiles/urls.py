# /home/mint/Desktop/ArtistMgntBack/app/profiles/urls.py
from django.urls import path
from .views import ManagerProfileByUserView,ManagerProfileCreateView,ManagerProfileListView,ManagerProfileDetailView,AllManagerProfileListView,UserProfileCreateView,UserProfileListView,UserProfileDetailView,AllUserProfileListView

app_name = "profiles"

urlpatterns = [
    # ... other URL patterns ...
    path("manager-by-user/<uuid:user_id>/", ManagerProfileByUserView.as_view(), name="manager-by-user"),
    path("user-profile/create/", UserProfileCreateView.as_view(), name="user-profile-create"),
    path("user-profile/list/", UserProfileListView.as_view(), name="user-profile-list"),
    path("user-profile/<uuid:pk>/", UserProfileDetailView.as_view(), name="user-profile-detail"),
    path("user-profile/all/", AllUserProfileListView.as_view(), name="user-profile-all"),
    path("manager-profile/create/", ManagerProfileCreateView.as_view(), name="manager-profile-create"),
    path("manager-profile/list/", ManagerProfileListView.as_view(), name="manager-profile-list"),
    path("manager-profile/<uuid:pk>/", ManagerProfileDetailView.as_view(), name="manager-profile-detail"),
    path("manager-profile/all/", AllManagerProfileListView.as_view(), name="manager-profile-all"),
]
