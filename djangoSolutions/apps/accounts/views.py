from rest_framework import viewsets, permissions
from .models import Organization, CustomUser
from .serializers import OrganizationSerializer, CustomUserSerializer
from django.db import models

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return CustomUser.objects.all()
        
        org = user.get_organization()
        if org:
            from djangoSolutions.apps.roles.models import OrganizationUser
            org_user_ids = OrganizationUser.objects.filter(organization=org).values_list('user_id', flat=True)
            return CustomUser.objects.filter(
                models.Q(organization=org) | models.Q(id__in=org_user_ids)
            ).distinct()
            
        return CustomUser.objects.filter(id=user.id)
