from rest_framework import serializers
from .models import Organization, CustomUser

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name', 'domain']

class CustomUserSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(read_only=True)
    organization_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    role = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'organization', 'organization_id', 'is_staff', 'is_superuser', 'is_active', 'address', 'contact_number', 'role']

    def get_role(self, obj):
        from djangoSolutions.apps.roles.models import OrganizationUser
        if obj.organization:
            org_user = OrganizationUser.objects.filter(user=obj, organization=obj.organization).first()
        else:
            org_user = OrganizationUser.objects.filter(user=obj).first()
            
        if org_user and org_user.role:
            return org_user.role.name.lower()
        return None

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'first_name', 'last_name', 'address', 'contact_number']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            address=validated_data.get('address', ''),
            contact_number=validated_data.get('contact_number', ''),
        )
        return user
