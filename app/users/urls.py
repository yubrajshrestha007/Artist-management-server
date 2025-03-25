from django.urls import path
from .views import (
    UserCreateView,
    UserListView,
    UserDetailView,
)

app_name = "users"

urlpatterns = [
    path("users/", UserListView.as_view(), name="user-list"),
    path("users-create/", UserCreateView.as_view(), name="user-list"),
    path("users/<uuid:pk>/", UserDetailView.as_view(), name="user-detail"),
]
