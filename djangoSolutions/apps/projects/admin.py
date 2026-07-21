from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "organization", "customer", "status", "budget", "created_by", "created_at")
    list_filter = ("organization", "status", "created_at")
    search_fields = ("name", "customer__name", "organization__name")
