from rest_framework import serializers
from .models import Role, OrganizationUser
from django.contrib.auth import get_user_model
from djangoSolutions.apps.accounts.models import Organization

User = get_user_model()


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ["id", "name"]


class OrganizationUserSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source="user.email", read_only=True)
    organization_name = serializers.CharField(source="organization.name", read_only=True)
    role_name = serializers.CharField(source="role.name", read_only=True)

    class Meta:
        model = OrganizationUser
        fields = [
            "id",
            "user",
            "user_email",
            "organization",
            "organization_name",
            "role",
            "role_name",
            "created_at",
        ]
