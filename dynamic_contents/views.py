# DRF
from rest_framework import mixins, filters
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Third Party
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# App
from dynamic_contents import pagination
from .serializers import FormatSerializer, PartSerializer
from .models import Format, Part, DynamicContent
from .serializers import DynamicContentSerializerMixin

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


class PartViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    BaseGenericViewSet
):
    queryset = Part.objects.all()
    serializer_class = PartSerializer
    search_fields = ['field', 'content', 'link']
    ordering_fields = ['created_at', 'type']
    filterset_fields = ['instance_id']


class DynamicContentView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'parts', openapi.IN_QUERY,
                description="Comma-separated list of part IDs",
                type=openapi.TYPE_STRING
            )
        ],
        responses={200: openapi.Response('Dynamic content response')}
    )
    def get(self, request, format_id):
        try:
            format_instance = Format.objects.get(pk=format_id)
            parts_ids = request.query_params.get('parts', '')

            # 쉼표로 분리하여 parts_ids를 리스트로 변환
            parts_ids_list = [int(pid) for pid in parts_ids.split(',') if pid.isdigit()]

            parts_instances = Part.objects.filter(id__in=parts_ids_list)

            # DynamicContent 인스턴스 생성
            dynamic_content = DynamicContent(format_instance, parts_instances)

            # DynamicContent 객체를 사용하여 최종 콘텐츠 생성
            response_data = DynamicContentSerializerMixin(dynamic_content).data
            return Response(response_data)
        except Format.DoesNotExist:
            return Response({"error": "Format not found"}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
