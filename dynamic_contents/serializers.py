# Django
from django.utils.translation import get_language

# DRF
from rest_framework import serializers

# App
from .models import Format, Part
from .utils import generate_text, generate_html, generate_i18n


class FormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Format
        fields = ['id', 'type', 'subtype', 'content']

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
        fields = ['id', 'field', 'content', 'link', 'instance_id']

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

        for part_representation in representation['parts']:
            # part_representation은 PartSerializer에서 반환된 사전 형식
            for field, part_info in part_representation.items():
                if field not in parts_dict:
                    parts_dict[field] = [part_info]  # 처음 나타난 field라면 배열로 초기화
                else:
                    parts_dict[field].append(part_info)  # 이미 존재하는 field라면 배열에 추가

        representation['parts'] = parts_dict

        representation['content_text'] = generate_text(instance.format, instance.parts.all())
        representation['content_i18n'] = generate_i18n(instance.format, instance.parts.all())
        representation['content_html'] = generate_html(instance.format, instance.parts.all())

        return representation
