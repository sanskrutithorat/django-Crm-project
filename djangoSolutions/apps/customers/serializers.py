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

    def to_representation(self, instance):
        rep = super().to_representation(instance)
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
