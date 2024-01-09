from rest_framework import serializers
from .models import Format, Part


class FormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Format
        fields = ['id', 'type', 'subtype', 'content']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # modeltranslation에 의해 생성된 필드 추가
        for field in ['content_en', 'content_ko', 'content_ja']:
            if hasattr(instance, field):
                representation[field] = getattr(instance, field)
        return representation


class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = ['id', 'field', 'content', 'link', 'instance_id']


class DynamicContentSerializerMixin:
    format = FormatSerializer(read_only=True)
    parts = PartSerializer(many=True, read_only=True)

    class Meta:
        fields = ['id', 'format', 'parts', 'content_text', 'content_html']
