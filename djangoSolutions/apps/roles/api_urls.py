from django.urls import path
from .views import (
    RoleListCreateView,
    RoleDetailView,
    AssignRoleView,
    OrganizationUserListView,
)

urlpatterns = [
    path("roles/", RoleListCreateView.as_view(), name="role-list-create"),
    path("roles/<int:pk>/", RoleDetailView.as_view(), name="role-detail"),

    path("assign-role/", AssignRoleView.as_view(), name="assign-role"),

    path("organization/<int:organization_id>/users/", 
         OrganizationUserListView.as_view(), 
         name="org-users"),
]
