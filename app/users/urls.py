from django.urls import path
from .views import (
    UserListView,
    UserDetailView,
    UserProfileCreateView,
    UserProfileListView,
    UserProfileDetailView,
)

app_name = "users"

urlpatterns = [
    path("users/", UserListView.as_view(), name="user-list"),
    path("users/<uuid:pk>/", UserDetailView.as_view(), name="user-detail"),
    # User Profile Endpoints
    path("user-profiles/", UserProfileCreateView.as_view(), name="user-profile-create"),
    path("user-profiles/list/", UserProfileListView.as_view(), name="user-profile-list"),
    path(
        "user-profiles/<uuid:pk>/",
        UserProfileDetailView.as_view(),
        name="user-profile-detail",
    ),
]
