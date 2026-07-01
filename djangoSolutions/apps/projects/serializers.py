from rest_framework import serializers
from .models import Project
from djangoSolutions.apps.customers.models import Customer

class ProjectSerializer(serializers.ModelSerializer):
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
            "organization",
            "created_by",
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

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if instance.customer:
            rep['customer'] = {
                'id': instance.customer.id,
                'name': instance.customer.name,
                'email': instance.customer.email
            }
        if instance.organization:
            rep['organization'] = {
                'id': instance.organization.id,
                'name': instance.organization.name
            }
        if instance.created_by:
            rep['created_by'] = {
                'id': instance.created_by.id,
                'email': instance.created_by.email
            }
        return rep
