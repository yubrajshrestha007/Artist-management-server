from django.urls import path
from .views import (
    RegisterView,
    LoginView,
)

app_name = "core"

urlpatterns = [
    # User Authentication
    path("login/", LoginView.as_view(), name="login"),
    # User Registration
    path("register/", RegisterView.as_view(), name="register"),
]
