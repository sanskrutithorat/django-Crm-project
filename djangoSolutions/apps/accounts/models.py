from django.db import models
from django.contrib.auth.models import AbstractUser

class Organization(models.Model):
    name = models.CharField(max_length=100)
    domain = models.CharField(max_length=100, unique=True, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"



class CustomUser(AbstractUser):
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, null=True, blank=True, related_name="users"
    )
    email = models.EmailField(unique=True)
    address = models.TextField(blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def get_organization(self):
        if self.organization:
            return self.organization
        from djangoSolutions.apps.roles.models import OrganizationUser
        org_user = OrganizationUser.objects.filter(user=self).select_related('organization').first()
        return org_user.organization if org_user else None

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"