from django.urls import path
from rest_framework.routers import DefaultRouter

# App
from dynamic_contents.views import ModelNameViewSet


# Variables
router = DefaultRouter()
router.register(r'model_names', ModelNameViewSet, basename='model_name')
urlpatterns = router.urls

urlpatterns += [
    # path('search', views.SearchView, name='regions'),
]
