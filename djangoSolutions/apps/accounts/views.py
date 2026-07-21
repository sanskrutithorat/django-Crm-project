from rest_framework import viewsets, permissions, generics
from .models import Organization, CustomUser
from .serializers import OrganizationSerializer, CustomUserSerializer
from django.db import models

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]

import django_filters
from django_filters import rest_framework as filters

class CustomUserFilter(filters.FilterSet):
    role = filters.CharFilter(field_name='org_memberships__role__name', lookup_expr='iexact')
    username = filters.CharFilter(field_name='username', lookup_expr='icontains')
    email = filters.CharFilter(field_name='email', lookup_expr='icontains')

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role']

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    filterset_class = CustomUserFilter
    search_fields = ['username', 'email']

    def get_queryset(self):
        user = self.request.user
        if getattr(self, 'swagger_fake_view', False) or user.is_anonymous:
            return CustomUser.objects.none()

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

    def perform_create(self, serializer):
        user_org = self.request.user.get_organization()
        org = None
        if self.request.user.is_superuser:
            org_id = self.request.data.get('organization_id')
            if org_id:
                from .models import Organization
                org = Organization.objects.filter(id=org_id).first()
        if not org:
            org = user_org

        user = serializer.save(organization=org)
        password = self.request.data.get('password', 'Pass@123')
        user.set_password(password)
        user.save()

        role_id = self.request.data.get('role_id')
        if role_id:
            from djangoSolutions.apps.roles.models import OrganizationUser
            OrganizationUser.objects.create(user=user, organization=user.organization, role_id=role_id)

    def perform_update(self, serializer):
        org = None
        if self.request.user.is_superuser:
            org_id = self.request.data.get('organization_id')
            if org_id:
                from .models import Organization
                org = Organization.objects.filter(id=org_id).first()
        
        if org:
            old_org = serializer.instance.organization
            user = serializer.save(organization=org)
            if old_org and old_org != org:
                from djangoSolutions.apps.roles.models import OrganizationUser
                OrganizationUser.objects.filter(user=user, organization=old_org).delete()
        else:
            user = serializer.save()
        
        password = self.request.data.get('password')
        if password and password.strip():
            user.set_password(password)
            user.save()

        role_id = self.request.data.get('role_id')
        if role_id:
            from djangoSolutions.apps.roles.models import OrganizationUser
            org_user, created = OrganizationUser.objects.get_or_create(
                user=user, 
                organization=user.organization,
                defaults={'role_id': role_id}
            )
            if not created:
                org_user.role_id = role_id
                org_user.save()
            
            # Unconditionally clean up any stale organization memberships
            OrganizationUser.objects.filter(user=user).exclude(organization=user.organization).delete()

class SuperadminListView(generics.ListAPIView):
    """
    Returns a list of all superadmin users.
    Only accessible by superadmins.
    """
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if not getattr(self.request.user, 'is_superuser', False):
            return CustomUser.objects.none()
        return CustomUser.objects.filter(is_superuser=True)
