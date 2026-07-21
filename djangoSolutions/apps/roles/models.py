from django.db import models
from django.contrib.auth import get_user_model
import uuid
from djangoSolutions.apps.accounts.models import Organization

User = get_user_model()


class Role(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="roles", null=True, blank=True)
    permissions = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["id"]
        unique_together = ("name", "organization")

    def __str__(self):
        return self.name


class OrganizationUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="org_memberships")
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="members")
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="assigned_users")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "organization")  # User cannot join same org twice
        ordering = ["id"]

    def __str__(self):
        return f"{self.user.email} - {self.organization.name} ({self.role.name})"
