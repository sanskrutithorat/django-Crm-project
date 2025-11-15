from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "id",
            "name",
            "email",
            "phone",
            "company_name",
            "organization",
            "created_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["organization", "created_by", "created_at", "updated_at"]
