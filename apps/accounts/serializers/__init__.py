from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from apps.accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "username", "first_name", "last_name", "role", "department", "phone", "is_active", "date_joined")
        read_only_fields = ("id", "date_joined")


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "username", "password", "password_confirm", "first_name", "last_name", "role", "department")

    def validate(self, attrs):
        if attrs["password"] != attrs.pop("password_confirm"):
            raise serializers.ValidationError({"password_confirm": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])

    def validate_old_password(self, value):
        if not self.context["request"].user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value
