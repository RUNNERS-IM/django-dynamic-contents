from rest_framework import serializers
from .models import Format, Part


class FormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Format
        fields = '__all__'


class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = '__all__'


class DynamicContentSerializerMixin:
    format = FormatSerializer(read_only=True)
    parts = PartSerializer(many=True, read_only=True)

    class Meta:
        fields = ['id', 'format', 'parts', 'content_text', 'content_html', 'created_at', 'updated_at']
