# Django Rest Framework
from rest_framework import mixins, filters
from rest_framework.viewsets import GenericViewSet

# Third Party
from django_filters.rest_framework import DjangoFilterBackend

# App
from dynamic_contents import pagination
from .serializers import FormatSerializer, PartSerializer, DynamicContentSerializer
from .models import Format, Part, DynamicContent


# Classes
class BaseGenericViewSet(GenericViewSet):
    filter_backends = [filters.OrderingFilter, filters.SearchFilter, DjangoFilterBackend]
    pagination_class = pagination.DefaultPagination


class FormatViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    BaseGenericViewSet
):
    queryset = Format.objects.all()
    serializer_class = FormatSerializer
    search_fields = ['type', 'content']
    ordering_fields = ['created_at', 'type']


class DynamicContentViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    BaseGenericViewSet
):
    queryset = DynamicContent.objects.all()
    serializer_class = DynamicContentSerializer
    search_fields = ['content']
    ordering_fields = ['created_at']
