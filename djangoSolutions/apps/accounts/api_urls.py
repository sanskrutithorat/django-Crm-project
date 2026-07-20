from django.urls import path, include
from rest_framework.routers import DefaultRouter
from djangoSolutions.apps.accounts.views import OrganizationViewSet, CustomUserViewSet, SuperadminListView
from djangoSolutions.apps.accounts.view.auth_views import LoginApiView, RefreshTokenApiView, ProfileApiView, LogoutApiView, RegisterApiView

router = DefaultRouter()
router.register(r'organizations', OrganizationViewSet)
router.register(r'users', CustomUserViewSet)

urlpatterns = [
    # main API endpoints
    *router.urls,
    path("superadmins/", SuperadminListView.as_view(), name="superadmins-list"),

    # authentication endpoints
    path("auth/register/", RegisterApiView.as_view(), name="register"),
    path("auth/login/", LoginApiView.as_view(), name="login"),
    path("auth/refresh/", RefreshTokenApiView.as_view(), name="refresh"),
    path("auth/profile/", ProfileApiView.as_view(), name="profile"), 
    path("auth/logout/", LogoutApiView.as_view(), name="logout"),


]