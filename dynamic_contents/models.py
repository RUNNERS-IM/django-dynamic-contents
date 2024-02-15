# Python
import re
import json
from collections import Counter

# Django
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from django.core.exceptions import ValidationError
from django.core.serializers.json import DjangoJSONEncoder


# Class Section
class BaseModel(models.Model):

    # Dates
    created_at = models.DateTimeField(_('생성일자'), auto_now_add=True, null=True)
    updated_at = models.DateTimeField(_('수정일자'), auto_now=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, self.id)


class FormatManager(models.Manager):
    def update_format_if_needed(self, format, defaults):
        updated = False
        for key, value in defaults.items():
            if not getattr(format, key):
                setattr(format, key, value)
                updated = True
        if updated:
            format.save()


# Format
class Format(BaseModel):

    type = models.CharField(_('Type (유형)'), max_length=100)
    subtype = models.CharField(_('Sub Type (세부 유형)'), max_length=100)
    content = models.TextField(_('Content (내용)'))  # "{user}가 {post}를 좋아요합니다."
    _placeholders = models.TextField(_('Placeholders'), blank=True, null=True)

    objects = FormatManager()

    class Meta:
        verbose_name = 'format'
        verbose_name_plural = 'formats'
        ordering = ['-created_at']

    def __str__(self):
        return '{}({}) {}'.format(self.__class__.__name__, self.id, self.content)

    def get_placeholders(self):
        """
        'placeholders' 필드를 배열로 변환하여 반환합니다.
        """
        if self._placeholders:
            return self._placeholders.split(',')
        return []

    def save(self, *args, **kwargs):
        # type과 subtype 필드를 대문자로 변환하고, _ 외의 특수문자 제거
        self.type = self.process_type_field(self.type)
        self.subtype = self.process_type_field(self.subtype)
        self._placeholders = self.extract_placeholders(self.content)

        placeholders = self.get_placeholders()
        placeholder_counts = Counter(placeholders)
        for placeholder, count in placeholder_counts.items():
            if count > 1:
                raise ValidationError(f'Placeholder "{{{placeholder}}}" used multiple times in content.')

        return super(Format, self).save(*args, **kwargs)

    @staticmethod
    def process_type_field(field_value):
        """
        필드 값을 대문자로 변환하고, _ 외의 특수문자를 제거합니다.
        """
        if field_value:
            return re.sub(r'[^A-Z_]', '', field_value.upper())
        return field_value

    @staticmethod
    def extract_placeholders(content):
        """
        주어진 content에서 '{{}}' 형식의 텍스트를 추출합니다.
        """
        if not content:
            return ''

        placeholders = re.findall(r'\{\{(\w+)\}\}', content)
        return ','.join(placeholders)


# Part
class Part(BaseModel):
    field = models.TextField(_('Field (필드)'), null=True, blank=True)  # user
    content = models.TextField(_('Content (내용)'), null=True, blank=True)  # 김선욱
    link = models.URLField(_('Link (링크)'), null=True, blank=True)  # https://runners.im/sun
    instance_id = models.TextField(_('Instance ID (인스턴스 ID)'), null=True, blank=True)  # 1

    class Meta:
        verbose_name = 'part'
        verbose_name_plural = 'parts'
        ordering = ['-created_at']

    def __str__(self):
        return '{}({}) {}'.format(self.__class__.__name__, self.id, self.content)

    def save(self, *args, **kwargs):
        super(Part, self).save(*args, **kwargs)


# Dynamic Content
class DynamicContentManagerMixin:

    def create_dynamic_content(self, format, parts):
        """
        Create a new DynamicContent object with the given format and parts.

        :param format: The Format object for the DynamicContent.
        :param parts: List of Part objects.
        :return: The created DynamicContent object.
        """
        # DynamicContent 객체 생성
        dynamic_content = self.create(format=format)

        # Part 객체들 연결
        for part in parts:
            dynamic_content.parts.add(part)

        return dynamic_content

    def update_dynamic_content(self, dynamic_content, format, parts):
        """
        Update the format and parts of the given DynamicContent object.

        :param dynamic_content: The DynamicContent object to update.
        :param format: The Format object for the DynamicContent.
        :param parts: List of Part objects.
        :return: The updated DynamicContent object.
        """
        # 기존 Part 객체들 삭제
        dynamic_content.parts.clear()

        # Part 객체들 연결
        for part in parts:
            dynamic_content.parts.add(part)

        # Format 업데이트
        dynamic_content.format = format

        # DynamicContent 저장
        dynamic_content.save()

        return dynamic_content


class DynamicContentModelMixin(models.Model):

    format = models.ForeignKey(Format, on_delete=models.SET_NULL, null=True, blank=True)
    parts = models.ManyToManyField(Part, blank=True)
    missing_placeholders = models.TextField(_('Missing Placeholders'), blank=True, null=True)

    class Meta:
        abstract = True

    def get_missing_placeholders(self):
        """
        이 메서드는 Format의 placeholders와 연결된 Parts가 모두 존재하는지 확인합니다.
        누락된 placeholders가 있다면 해당 placeholders를 리스트로 반환합니다.
        """
        if not self.format:
            return []  # Format이 설정되지 않은 경우 빈 리스트 반환

        placeholders = self.format.get_placeholders()
        parts_fields = [part.field for part in self.parts.all()]
        missing_placeholders = list(set(placeholders) - set(parts_fields))

        return missing_placeholders

    def _get_format_string(self):
        """
        현재 언어에 맞는 format 문자열을 반환합니다.
        """
        if not self.format:
            return ''

        current_language = get_language()
        content_field = f"content_{current_language}"
        return getattr(self.format, content_field, self.format.content)

    def get_text(self):
        format_string = self._get_format_string()
        if not format_string:
            return ''

        for part in self.parts.all():
            format_string = format_string.replace("{{" + part.field + "}}", part.content or '')
        return format_string

    def get_i18n(self):
        format_string = self._get_format_string()
        if not format_string:
            return ''

        # 플레이스홀더를 찾아서 순서대로 인덱스 매핑
        placeholders = re.findall(r'\{\{(\w+)\}\}', format_string)
        index_map = {placeholder: idx for idx, placeholder in enumerate(placeholders)}

        # Part 객체를 순회하며 필드를 대체 문자열로 변환
        for part in self.parts.all():
            if part.field in index_map:
                idx = index_map[part.field]
                replacement = f'<{idx}>{part.content}</{idx}>'
                placeholder = f"{{{{{part.field}}}}}"
                format_string = format_string.replace(placeholder, replacement, 1)  # 한 번만 대체

        return format_string

    def get_html(self):
        format_string = self._get_format_string()
        if not format_string:
            return ''

        # Part 객체를 순회하며 필드를 대체 문자열로 변환
        for part in self.parts.all():
            # 링크가 있거나 없거나 항상 <a> 태그를 사용
            link = part.link or '#'
            replacement = f'<a class="{part.field}" href="{link}">{part.content}</a>'

            placeholder = f"{{{{{part.field}}}}}"
            format_string = format_string.replace(placeholder, replacement)

        return format_string

    def save(self, *args, **kwargs):
        # Update the missing_placeholders field before saving
        missing = self.get_missing_placeholders()
        self.missing_placeholders = json.dumps(missing, cls=DjangoJSONEncoder)

        super(DynamicContentModelMixin, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        DynamicContent를 삭제하기 전에 관련된 모든 파트를 삭제합니다.
        """
        self.parts.all().delete()
        super(DynamicContentModelMixin, self).delete(*args, **kwargs)
