from rest_framework import viewsets, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Customer
from .serializers import CustomerSerializer

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Customer
from .serializers import CustomerSerializer
from django.shortcuts import get_object_or_404

class CustomerViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for customers with consistent JSON responses.
    Only allows users to manage customers within their organization.
    """
    serializer_class = CustomerSerializer
    from djangoSolutions.apps.roles.permissions import CustomerAccessPermission
    permission_classes = [permissions.IsAuthenticated, CustomerAccessPermission]
    authentication_classes = [JWTAuthentication]

    filterset_fields = {
        'company_name': ['icontains'],
        'projects': ['exact'],
    }
    search_fields = ['name', 'email', 'company_name']
    ordering_fields = ['created_at', 'name']

    # -----------------------------------------------------------
    # Get all customers (GET /api/customers/)
    # -----------------------------------------------------------
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False) or getattr(self.request.user, 'is_anonymous', True):
            return Customer.objects.none()
        if self.request.user.is_superuser:
            return Customer.objects.all().select_related('organization', 'created_by')
        return Customer.objects.filter(
            organization=self.request.user.get_organization()
        ).select_related('organization', 'created_by')

    # -----------------------------------------------------------
    # Create new customer (POST)
    # -----------------------------------------------------------
    def perform_create(self, serializer):
        serializer.save(
            organization=self.request.user.get_organization(),
            created_by=self.request.user,
        )
