from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "organization", "created_by", "created_at")
    list_filter = ("organization",)
    search_fields = ("name", "email", "company_name", "organization__name")
