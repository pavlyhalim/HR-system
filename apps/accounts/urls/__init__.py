from django.urls import path

from apps.accounts.views import (
    ChangePasswordView,
    LoginView,
    ProfileView,
    RegisterView,
    TokenRefresh,
    UserListView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="auth-register"),
    path("login/", LoginView.as_view(), name="auth-login"),
    path("token/refresh/", TokenRefresh.as_view(), name="auth-token-refresh"),
    path("profile/", ProfileView.as_view(), name="auth-profile"),
    path("change-password/", ChangePasswordView.as_view(), name="auth-change-password"),
    path("users/", UserListView.as_view(), name="user-list"),
]
