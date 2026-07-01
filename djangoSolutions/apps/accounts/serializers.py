from rest_framework import serializers
from .models import Organization, CustomUser

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name', 'domain']

class CustomUserSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'organization', 'is_staff', 'is_active', 'address', 'contact_number']

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
