# /home/mint/Desktop/ArtistMgntBack/app/profiles/urls.py

from django.urls import path
from .views import (
    AllUserProfileListView,
    UserProfileCreateView,
    UserProfileListView,
    UserProfileDetailView,
    ManagerProfileCreateView,
    ManagerProfileListView,
    ManagerProfileDetailView,
    AllManagerProfileListView,
)

app_name = "profiles"

urlpatterns = [
    # User Profile Endpoints
    path("user-profiles/", UserProfileCreateView.as_view(), name="user-profile-create"),
    path('all-profiles/', AllUserProfileListView.as_view()),

    path("user-profiles/list/", UserProfileListView.as_view(), name="user-profile-list"),
    path(
        "user-profiles/<uuid:pk>/",
        UserProfileDetailView.as_view(),
        name="user-profile-detail",
    ),
    # Manager Profile Endpoints
    path("manager-profiles/", ManagerProfileCreateView.as_view(), name="manager-profile-create"),
    path("manager-profiles/list/", ManagerProfileListView.as_view(), name="manager-profile-list"),
    path("manager-profiles/all/", AllManagerProfileListView.as_view(), name="manager-profile-all"),
    path(
        "manager-profiles/<uuid:pk>/",
        ManagerProfileDetailView.as_view(),
        name="manager-profile-detail",
    ),
]
