from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "project", "status", "assigned_to", "organization", "due_date")
    list_filter = ("status", "organization", "project")
    search_fields = ("title", "project__name", "assigned_to__email")
