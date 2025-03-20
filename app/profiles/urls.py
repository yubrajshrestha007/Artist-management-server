from django.urls import path
from .views import (
    AllUserProfileListView,
    UserProfileCreateView,
    UserProfileListView,
    UserProfileDetailView,
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
]
