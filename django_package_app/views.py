# Django Rest Framework
from rest_framework import mixins, filters
from rest_framework.viewsets import GenericViewSet

# Third Party
from django_filters.rest_framework import DjangoFilterBackend

# App
from django_package_app import serializers, pagination
from django_package_app.models import ModelName

# Variables
name_search_fields = ['name', 'name_en', 'name_ja', 'name_ko']


# Classes
class BaseGenericViewSet(GenericViewSet):
    search_fields = name_search_fields
    filter_backends = [filters.OrderingFilter, filters.SearchFilter, DjangoFilterBackend]
    pagination_class = pagination.DefaultPagination


class ModelNameViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    BaseGenericViewSet
):
    queryset = ModelName.objects.all()
    serializer_class = serializers.ModelNameSerializer

    search_fields = ('title',)
    ordering_fields = ('id', 'created',)
    filterset_fields = []
