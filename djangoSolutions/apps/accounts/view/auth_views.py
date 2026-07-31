from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import serializers
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# --------------------------------------------------------------------
# Custom serializer to allow login using EMAIL instead of username
# --------------------------------------------------------------------
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT serializer that allows authentication with email + password
    instead of username + password.
    """
    @classmethod
    def get_token(cls, user):
        # Use the parent method to generate standard tokens
        token = super().get_token(user)
        # Add custom claims (extra info inside the token)
        token['email'] = user.email
        token['organization'] = user.organization.name if user.organization else None
        return token


# --------------------------------------------------------------------
# Login View
# --------------------------------------------------------------------
class LoginApiView(TokenObtainPairView):
    """
    Handles user login and returns JWT access + refresh tokens.
    """
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        """
        POST /api/auth/login/
        Expected JSON: { "email": "user@example.com", "password": "mypassword" }
        """
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response(
                {"error": "Invalid email or password"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        user = serializer.user
        from djangoSolutions.apps.roles.permissions import get_user_role
        from djangoSolutions.apps.roles.models import OrganizationUser
        
        if user.is_superuser:
            role = "Super Admin"
        else:
            role_obj = get_user_role(user)
            role = role_obj.name if role_obj else None

        org_name = None
        if user.organization:
            org_name = user.organization.name
        else:
            org_user = OrganizationUser.objects.filter(user=user).first()
            if org_user and org_user.organization:
                org_name = org_user.organization.name

        response_data = serializer.validated_data
        response_data['user'] = {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "organization": org_name,
            "role": role,
            "is_active": user.is_active,
            "address": user.address,
            "contact_number": user.contact_number,
        }

        return Response(response_data, status=status.HTTP_200_OK)


# --------------------------------------------------------------------
# Refresh Token View
# --------------------------------------------------------------------
class RefreshTokenApiView(TokenRefreshView):
    """
    Handles refreshing access tokens using a refresh token.
    """
    def post(self, request, *args, **kwargs):
        """
        POST /api/auth/refresh/
        Expected JSON: { "refresh": "<your_refresh_token>" }
        """
        return super().post(request, *args, **kwargs)
    

# -------------------------------
# Serializer for logout endpoint
# -------------------------------
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(help_text="Refresh token to blacklist")


# -------------------------------
# Logout view
# -------------------------------
# -------------------------------
# Logout view (with Swagger schema)
# -------------------------------
class LogoutApiView(APIView):
    """
    Logs out the user by blacklisting their refresh token.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = LogoutSerializer

    @swagger_auto_schema(
    request_body=LogoutSerializer,
    responses={
        200: openapi.Response("Successfully logged out."),
        400: openapi.Response("Invalid or expired token."),
    }
)
    def post(self, request):
        """
        POST /api/auth/logout/
        Expected JSON: { "refresh": "<your_refresh_token>" }
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh_token = serializer.validated_data["refresh"]

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
        except TokenError:
            return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

# --------------------------------------------------------------------
# Register View
# --------------------------------------------------------------------
from rest_framework.permissions import AllowAny
from djangoSolutions.apps.accounts.serializers import RegisterSerializer

class RegisterApiView(APIView):
    """
    Registers a new user in the system.
    """
    permission_classes = [AllowAny]
    authentication_classes = []

    @swagger_auto_schema(
        request_body=RegisterSerializer,
        responses={201: openapi.Response("User created")}
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully", "user": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {"error": "Registration failed", "details": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

# --------------------------------------------------------------------
# Profile View
# -------------------------------------------------------------------- 
User = get_user_model()
class ProfileApiView(APIView):
    """
    Returns the logged-in user's profile data.
    Requires JWT authentication.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user = request.user
        from djangoSolutions.apps.roles.permissions import get_user_role
        from djangoSolutions.apps.roles.models import OrganizationUser
        
        if user.is_superuser:
            role = "Super Admin"
        else:
            role_obj = get_user_role(user)
            role = role_obj.name if role_obj else None

        org_name = None
        if user.organization:
            org_name = user.organization.name
        else:
            org_user = OrganizationUser.objects.filter(user=user).first()
            if org_user and org_user.organization:
                org_name = org_user.organization.name

        return Response({
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "organization": org_name,
            "role": role,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_staff": user.is_staff,
            "is_active": user.is_active,
            "address": user.address,
            "contact_number": user.contact_number,
        }, status=status.HTTP_200_OK)

# # djangoSolutions/apps/accounts/view/auth_view.py

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.contrib.auth import authenticate
# from django.contrib.auth import get_user_model

# User = get_user_model()

# class LoginApiView(APIView):
#     """
#     Handles user login and returns JWT access and refresh tokens.
#     """

#     def post(self, request):
#         email = request.data.get('email')
#         password = request.data.get('password')

#         if not email or not password:
#             return Response({"error": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

#         user = authenticate(request, email=email, password=password)
#         if user is not None:
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 "refresh": str(refresh),
#                 "access": str(refresh.access_token),
#                 "user": {
#                     "id": user.id,
#                     "email": user.email,
#                     "username": user.username,
#                     "organization": user.organization.name if user.organization else None,
#                 }
#             })
#         return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


# class RefreshTokenApiView(APIView):
#     """
#     Allows refreshing of JWT tokens.
#     """

#     def post(self, request):
#         refresh_token = request.data.get('refresh')

#         if not refresh_token:
#             return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             refresh = RefreshToken(refresh_token)
#             access_token = str(refresh.access_token)
#             return Response({"access": access_token})
#         except Exception:
#             return Response({"error": "Invalid or expired refresh token"}, status=status.HTTP_400_BAD_REQUEST)
