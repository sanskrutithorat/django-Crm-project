from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    from djangoSolutions.apps.roles.permissions import TaskAccessPermission
    permission_classes = [IsAuthenticated, TaskAccessPermission]
    authentication_classes = [JWTAuthentication]

    filterset_fields = ['status', 'project', 'assigned_to']
    search_fields = ['title', 'description']
    ordering_fields = ['due_date', 'created_at']

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False) or getattr(self.request.user, 'is_anonymous', True):
            return Task.objects.none()
        
        return Task.objects.filter(
            organization=self.request.user.get_organization()
        ).select_related("project", "assigned_to", "created_by")

    def perform_create(self, serializer):
        serializer.save(
            organization=self.request.user.get_organization(),
            created_by=self.request.user,
        )
