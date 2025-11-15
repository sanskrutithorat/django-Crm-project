from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Role, OrganizationUser
from .serializers import RoleSerializer, OrganizationUserSerializer


# ---------------------------
# ROLE CRUD
# ---------------------------
class RoleListCreateView(generics.ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]


class RoleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]


# ---------------------------
# ASSIGN USER TO ORGANIZATION
# ---------------------------
class AssignRoleView(generics.CreateAPIView):
    serializer_class = OrganizationUserSerializer
    permission_classes = [IsAuthenticated]

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
