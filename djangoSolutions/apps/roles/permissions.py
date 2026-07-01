from rest_framework import permissions
from .models import OrganizationUser

def get_user_role(user):
    """
    Helper function to get the role of the user in their organization.
    Returns the role name (e.g., 'admin', 'manager', 'employee', 'viewer')
    or None if no role is found.
    """
    if not user.is_authenticated:
        return None
    
    # If user.organization is set, use it. Otherwise, find their first OrganizationUser record.
    if user.organization:
        org_user = OrganizationUser.objects.filter(user=user, organization=user.organization).first()
    else:
        org_user = OrganizationUser.objects.filter(user=user).first()
        
    if org_user and org_user.role:
        return org_user.role.name.lower()
    return None

class CustomerAccessPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Everyone in the org can GET (view) customers
        if request.method in permissions.SAFE_METHODS:
            return True
            
        role = get_user_role(request.user)
        # Only admin and manager can POST, PUT, PATCH, DELETE customers
        return role in ['admin', 'manager']

class ProjectAccessPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
            
        # Everyone in the org can GET (view) projects
        if request.method in permissions.SAFE_METHODS:
            return True
            
        role = get_user_role(request.user)
        # Only admin and manager can POST, PUT, PATCH, DELETE projects
        return role in ['admin', 'manager']

class TaskAccessPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
            
        # Everyone in the org can GET (view) tasks
        if request.method in permissions.SAFE_METHODS:
            return True
            
        role = get_user_role(request.user)
        
        if request.method == 'DELETE':
            # Only admin and manager can DELETE tasks
            return role in ['admin', 'manager']
            
        # Admin, manager, and employee can POST, PUT, PATCH tasks
        return role in ['admin', 'manager', 'employee']

class RoleAssignmentPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
            
        role = get_user_role(request.user)
        # Only admins can assign or modify roles
        return role == 'admin'
