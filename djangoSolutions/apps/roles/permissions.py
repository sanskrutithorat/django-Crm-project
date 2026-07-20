from rest_framework import permissions
from .models import OrganizationUser

def get_user_role(user):
    """
    Helper function to get the Role object of the user in their organization.
    Returns the Role instance or None.
    """
    if not user.is_authenticated:
        return None
    
    if user.organization:
        org_user = OrganizationUser.objects.filter(user=user, organization=user.organization).select_related('role').first()
    else:
        org_user = OrganizationUser.objects.filter(user=user).select_related('role').first()
        
    if org_user and org_user.role:
        return org_user.role
    return None

class DynamicRBACPermission(permissions.BasePermission):
    module_name = None  # e.g., 'customers'

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
            
        # Superadmins bypass all checks
        if getattr(request.user, 'is_superuser', False):
            return True
            
        role = get_user_role(request.user)
        if not role:
            return False
            
        # Admins have full access within their org
        if role.name.lower() == 'admin':
            return True
            
        if not self.module_name:
            return False
            
        # Parse JSON permissions
        perms = role.permissions.get(self.module_name, [])
        
        if request.method in permissions.SAFE_METHODS:
            return 'read' in perms
        elif request.method == 'POST':
            return 'create' in perms
        elif request.method in ['PUT', 'PATCH']:
            return 'update' in perms
        elif request.method == 'DELETE':
            return 'delete' in perms
            
        return False

class CustomerAccessPermission(DynamicRBACPermission):
    module_name = 'customers'

class ProjectAccessPermission(DynamicRBACPermission):
    module_name = 'projects'

class TaskAccessPermission(DynamicRBACPermission):
    module_name = 'tasks'

class RoleAssignmentPermission(DynamicRBACPermission):
    module_name = 'roles'

