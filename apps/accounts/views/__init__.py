from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.accounts.models import User
from apps.accounts.serializers import ChangePasswordSerializer, RegisterSerializer, UserSerializer

# Aliases used by URL config
LoginView = TokenObtainPairView
TokenRefresh = TokenRefreshView


class RegisterView(generics.CreateAPIView):
    """Register a new user."""

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class ProfileView(generics.RetrieveUpdateAPIView):
    """Get or update the current user's profile."""

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class ChangePasswordView(APIView):
    """Change the current user's password."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data["new_password"])
        request.user.save(update_fields=["password"])
        return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)


class UserListView(generics.ListAPIView):
    """List all users (HR/Admin only)."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_fields = ["role", "department", "is_active"]
    search_fields = ["email", "first_name", "last_name"]
    ordering_fields = ["date_joined", "email", "role"]


class LoginView(TokenObtainPairView):
    """JWT Token login."""

    pass


class TokenRefresh(TokenRefreshView):
    """JWT Token refresh."""

    pass
