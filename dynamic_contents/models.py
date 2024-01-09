# Django
import re

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language


# Class Section
class BaseModel(models.Model):

    # Dates
    created_at = models.DateTimeField(_('생성일자'), auto_now_add=True, null=True)
    updated_at = models.DateTimeField(_('수정일자'), auto_now=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, self.id)


# Format
class Format(BaseModel):

    type = models.CharField(_('Type (유형)'), max_length=100)
    subtype = models.CharField(_('Sub Type (세부 유형)'), max_length=100, null=True, blank=True)
    content = models.TextField(_('Content (내용)'))  # "{user}가 {post}를 좋아요합니다."

    class Meta:
        verbose_name = 'format'
        verbose_name_plural = 'formats'
        ordering = ['-created_at']

    def __str__(self):
        return '{}'.format(self.content)


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
        return '{}'.format(self.content)

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

    format = models.ForeignKey(Format, on_delete=models.CASCADE, related_name='contents')
    parts = models.ManyToManyField(Part, related_name='contents')

    class Meta:
        abstract = True

    def __str__(self):
        return '{}'.format(self.content_text)

    def get_text(self):
        current_language = get_language()
        content_field = f"content_{current_language}"
        format_string = getattr(self.format, content_field, self.format.content)

        for part in self.parts.all():
            format_string = format_string.replace("{{" + part.field + "}}", part.content or '')
        return format_string

    def get_html(self):
        current_language = get_language()
        content_field = f"content_{current_language}"
        format_string = getattr(self.format, content_field, self.format.content)

        # Part 객체를 순회하며 필드를 대체 문자열로 변환
        for idx, part in enumerate(self.parts.all()):
            replacement = part.content or ''
            if part.link:
                replacement = f'<a href="{part.link}">{replacement}</a>'
            placeholder = f"{{{{{part.field}}}}}"
            format_string = format_string.replace(placeholder, f'<{idx}>{replacement}</{idx}>')

        return format_string

    def save(self, *args, **kwargs):
        self.content_text = self.get_text()
        self.content_html = self.get_html()
        super(DynamicContentModelMixin, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        DynamicContent를 삭제하기 전에 관련된 모든 파트를 삭제합니다.
        """
        self.parts.all().delete()
        super(DynamicContentModelMixin, self).delete(*args, **kwargs)
