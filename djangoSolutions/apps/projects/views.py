from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import Http404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import Http404
from .models import Project
from .serializers import ProjectSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    from djangoSolutions.apps.roles.permissions import ProjectAccessPermission
    permission_classes = [permissions.IsAuthenticated, ProjectAccessPermission]
    authentication_classes = [JWTAuthentication]

    filterset_fields = ['status', 'customer']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'start_date', 'budget']

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False) or getattr(self.request.user, 'is_anonymous', True):
            return Project.objects.none()
            
        if self.request.user.is_superuser:
            return Project.objects.all().select_related('customer', 'organization', 'created_by')
            
        # only projects for the user's organization
        return Project.objects.filter(
            organization=self.request.user.get_organization()
        ).select_related('customer', 'organization', 'created_by')

    def perform_create(self, serializer):
        serializer.save(
            organization=self.request.user.get_organization(),
            created_by=self.request.user,
        )
