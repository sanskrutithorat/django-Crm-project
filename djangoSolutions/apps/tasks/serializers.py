from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "due_date",
            "project",
            "assigned_to",
            "created_by",
            "organization",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["organization", "created_by"]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if instance.project:
            rep['project'] = {
                'id': instance.project.id,
                'name': instance.project.name
            }
        if instance.assigned_to:
            rep['assigned_to'] = {
                'id': instance.assigned_to.id,
                'email': instance.assigned_to.email,
                'username': instance.assigned_to.username
            }
        if instance.created_by:
            rep['created_by'] = {
                'id': instance.created_by.id,
                'email': instance.created_by.email
            }
        if instance.organization:
            rep['organization'] = {
                'id': instance.organization.id,
                'name': instance.organization.name
            }
        return rep
