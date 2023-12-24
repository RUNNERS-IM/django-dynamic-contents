from rest_framework import serializers
from .models import Format, Part, DynamicContent


class FormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Format
        fields = '__all__'


class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = '__all__'


class DynamicContentSerializer(serializers.ModelSerializer):
    parts = PartSerializer(many=True, read_only=True)

    class Meta:
        model = DynamicContent
        fields = ['id', 'format', 'parts', 'content']
