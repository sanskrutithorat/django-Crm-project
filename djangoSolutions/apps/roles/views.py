from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Role, OrganizationUser
from .serializers import RoleSerializer, OrganizationUserSerializer


# ---------------------------
# ROLE CRUD
# ---------------------------
from djangoSolutions.apps.roles.permissions import RoleAssignmentPermission

class RoleListCreateView(generics.ListCreateAPIView):
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated, RoleAssignmentPermission]
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False) or getattr(self.request.user, 'is_anonymous', True):
            return Role.objects.none()
            
        if self.request.user.is_superuser:
            return Role.objects.all()
            
        # Only return roles for the user's organization
        return Role.objects.filter(organization=self.request.user.get_organization())

    def perform_create(self, serializer):
        serializer.save(organization=self.request.user.get_organization())

class RoleDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated, RoleAssignmentPermission]
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False) or getattr(self.request.user, 'is_anonymous', True):
            return Role.objects.none()
            
        if self.request.user.is_superuser:
            return Role.objects.all()
            
        return Role.objects.filter(organization=self.request.user.get_organization())


# ---------------------------
# ASSIGN USER TO ORGANIZATION
# ---------------------------
class AssignRoleView(generics.CreateAPIView):
    serializer_class = OrganizationUserSerializer
    from djangoSolutions.apps.roles.permissions import RoleAssignmentPermission
    permission_classes = [IsAuthenticated, RoleAssignmentPermission]

    def create(self, request, *args, **kwargs):
        user_id = request.data.get("user")
        organization_id = request.data.get("organization")
        role_id = request.data.get("role")

        if not (user_id and organization_id and role_id):
            return Response(
                {"success": False, "message": "user, organization, role are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        org_user, created = OrganizationUser.objects.update_or_create(
            user_id=user_id,
            organization_id=organization_id,
            defaults={"role_id": role_id},
        )

        serializer = self.get_serializer(org_user)
        return Response({"success": True, "data": serializer.data})
        

# ---------------------------
# LIST ALL USERS IN ORG
# ---------------------------
class OrganizationUserListView(generics.ListAPIView):
    serializer_class = OrganizationUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        org_id = self.kwargs["organization_id"]
        return OrganizationUser.objects.filter(organization_id=org_id)
