from rest_framework import serializers
from .models import Task
from djangoSolutions.apps.projects.models import Project
from djangoSolutions.apps.accounts.models import CustomUser

class TaskSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source="project.name", read_only=True)
    assigned_to_email = serializers.CharField(source="assigned_to.email", read_only=True)
    created_by_email = serializers.CharField(source="created_by.email", read_only=True)
    organization_name = serializers.CharField(source="organization.name", read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "due_date",
            "project",
            "project_name",
            "assigned_to",
            "assigned_to_email",
            "created_by",
            "created_by_email",
            "organization",
            "organization_name",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["organization", "created_by"]
