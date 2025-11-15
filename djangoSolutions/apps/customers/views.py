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
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    # -----------------------------------------------------------
    # Get all customers (GET /api/customers/)
    # -----------------------------------------------------------
    def get_queryset(self):
        return Customer.objects.filter(organization=self.request.user.organization)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "success": True,
            "count": len(serializer.data),
            "customers": serializer.data
        }, status=status.HTTP_200_OK)

    # -----------------------------------------------------------
    # Get one customer (GET /api/customers/{id}/)
    # -----------------------------------------------------------
    def retrieve(self, request, *args, **kwargs):
        instance = get_object_or_404(self.get_queryset(), pk=kwargs.get("pk"))
        serializer = self.get_serializer(instance)
        return Response({
            "success": True,
            "customer": serializer.data
        }, status=status.HTTP_200_OK)

    # -----------------------------------------------------------
    # Create new customer (POST)
    # -----------------------------------------------------------
    def perform_create(self, serializer):
        serializer.save(
            organization=self.request.user.organization,
            created_by=self.request.user,
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({
                "success": True,
                "message": "Customer created successfully.",
                "customer": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    # -----------------------------------------------------------
    # Update customer (PUT)
    # -----------------------------------------------------------
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response({
                "success": True,
                "message": "Customer updated successfully.",
                "customer": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    # -----------------------------------------------------------
    # Partial update (PATCH)
    # -----------------------------------------------------------
    # ✅ Add this for custom PATCH handling
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Customer updated successfully.",
                "customer": serializer.data
            })
        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=400)


    # -----------------------------------------------------------
    # Delete customer (DELETE)
    # -----------------------------------------------------------
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "success": True,
            "message": "Customer deleted successfully."
        }, status=status.HTTP_200_OK)
