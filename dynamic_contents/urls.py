from django.urls import path
from rest_framework.routers import DefaultRouter

# App
from dynamic_contents.views import FormatViewSet, PartViewSet


# Variables
router = DefaultRouter()
router.register(r'formats', FormatViewSet)
router.register(r'parts', PartViewSet)
urlpatterns = router.urls

urlpatterns += []
