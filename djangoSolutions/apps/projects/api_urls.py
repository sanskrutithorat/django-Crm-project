from rest_framework.routers import DefaultRouter
from djangoSolutions.apps.projects.views import ProjectViewSet

router = DefaultRouter()
router.register(r"projects", ProjectViewSet, basename="project")

urlpatterns = router.urls
