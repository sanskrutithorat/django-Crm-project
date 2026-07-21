from django.contrib import admin
from .models import Role, OrganizationUser

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)

@admin.register(OrganizationUser)
class OrganizationUserAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "organization", "role", "created_at")
    list_filter = ("organization", "role")
    search_fields = ("user__email", "organization__name", "role__name")
