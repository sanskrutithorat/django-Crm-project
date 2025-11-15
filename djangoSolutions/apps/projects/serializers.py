from rest_framework import serializers
from .models import Project
from djangoSolutions.apps.customers.models import Customer  # safe if path resolves; adjust import if needed



class ProjectSerializer(serializers.ModelSerializer):
    # extra display fields
    customer_name = serializers.CharField(source="customer.name", read_only=True)
    organization_name = serializers.CharField(source="organization.name", read_only=True)
    created_by_username = serializers.CharField(source="created_by.username", read_only=True)

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "description",
            "status",
            "budget",
            "start_date",
            "end_date",
            "customer",
            "customer_name",
            "organization",
            "organization_name",
            "created_by",
            "created_by_username",
            "created_at",
            "updated_at"
        ]
        read_only_fields = ["organization", "created_by", "created_at", "updated_at"]

    def validate_customer(self, value):
        """
        Ensure the provided customer belongs to the same organization
        as the request user (if request present).
        """
        request = self.context.get("request")
        if request and hasattr(request, "user") and request.user.is_authenticated:
            user_org = request.user.organization
            if value.organization != user_org:
                raise serializers.ValidationError("That customer does not belong to your organization.")
        return value
