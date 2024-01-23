from rest_framework import serializers
from .models import Format, Part
from django.utils.translation import get_language


class FormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Format
        fields = ['type', 'subtype', 'content']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        current_language = get_language()
        content_field = f"content_{current_language}"

        if hasattr(instance, content_field):
            representation['content'] = getattr(instance, content_field)
        else:
            representation['content'] = instance.content

        return representation


class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = ['field', 'content', 'link', 'instance_id']

    def to_representation(self, instance):
        # Part 객체를 필드 이름을 키로 사용하는 사전으로 변환
        return {
            instance.field: {
                'content': instance.content,
                'link': instance.link,
                'instance_id': instance.instance_id
            }
        }


class DynamicContentSerializerMixin(serializers.Serializer):
    format = FormatSerializer(read_only=True)
    parts = PartSerializer(many=True, read_only=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        parts_dict = {}

        for part in representation['parts']:
            parts_dict.update(part)

        representation['parts'] = parts_dict
        representation['content_text'] = instance.get_text()
        representation['content_i18n'] = instance.get_i18n()
        representation['content_html'] = instance.get_html()

        return representation
