# Django
import re

from django.conf import settings
from django.db import models


# Class Section
class BaseModel(models.Model):

    # Dates
    created_at = models.DateTimeField('생성일자', auto_now_add=True, null=True)
    updated_at = models.DateTimeField('수정일자', auto_now=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, self.id)


# Format
class Format(BaseModel):

    type = models.CharField('Type (유형)', max_length=100)
    content = models.TextField('Content (내용)')  # "{user}가 {post}를 좋아요합니다."

    class Meta:
        verbose_name = 'format'
        verbose_name_plural = 'formats'
        ordering = ['-created_at']

    def __str__(self):
        return '{}'.format(self.content)


# Part
class Part(BaseModel):
    field = models.TextField('Field (필드)', null=True, blank=True)  # user
    content = models.TextField('Content (내용)', null=True, blank=True)  # 김선욱
    link = models.URLField('Link (링크)', null=True, blank=True)  # https://runners.im/sun
    instance_id = models.TextField('Instance ID (인스턴스 ID)', null=True, blank=True)  # 1

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


class DynamicContentModelMixin:

    format = models.ForeignKey(Format, on_delete=models.CASCADE, related_name='contents')
    parts = models.ManyToManyField(Part, related_name='contents')

    content_text = models.TextField('Text Content', null=True, blank=True)
    content_html = models.TextField('Html Content', null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return '{}'.format(self.content_text)

    def save(self, *args, **kwargs):
        super(DynamicContentModelMixin, self).save(*args, **kwargs)

    def validate_parts_with_format(self):
        required_fields = re.findall(r"\{(\w+)\}", self.format.content)
        for field in required_fields:
            if not self.parts.filter(field=field).exists():
                raise ValueError(f"필수 파트 '{field}'가 누락되었습니다.")

    @property
    def text(self):
        format_string = self.format.content
        for part in self.parts.all():
            format_string = format_string.replace("{" + part.field + "}", part.content or '')
        if self.content_text != format_string:
            self.content_text = format_string
            self.save(update_fields=['content_text'])
        return format_string

    @property
    def html(self):
        format_string = self.format.content
        for part in self.parts.all():
            replacement = part.content or ''
            if part.link:
                replacement = f'<a href="{part.link}">{replacement}</a>'
            format_string = format_string.replace("{" + part.field + "}", replacement)
        if self.content_html != format_string:
            self.content_html = format_string
            self.save(update_fields=['content_html'])
        return format_string

    def add_part(self, field, content, link=None, instance_id=None):
        """
        새로운 Part를 이 DynamicContent에 추가합니다.

        사용 예시:
        dynamic_content = DynamicContent.objects.get(id=some_id)
        new_part = dynamic_content.add_part(field='new_field', content='new content')
        """
        part = Part.objects.create(field=field, content=content, link=link, instance_id=instance_id)
        self.parts.add(part)
        return part

    def update_parts(self, parts_data):
        """
        이 DynamicContent의 모든 Part를 업데이트합니다.
        parts_data는 각 Part에 대한 데이터를 담은 딕셔너리의 리스트입니다.

        사용 예시:
        parts_data = [{'field': 'field1', 'content': 'content1'}, {'field': 'field2', 'content': 'content2'}]
        dynamic_content.update_parts(parts_data)
        """
        self.parts.clear()
        for data in parts_data:
            part = Part.objects.create(**data)
            self.parts.add(part)
        self.save()  # DynamicContent 업데이트

    def delete(self, *args, **kwargs):
        """
        DynamicContent를 삭제하기 전에 관련된 모든 파트를 삭제합니다.
        """
        self.parts.all().delete()
        super(DynamicContentModelMixin, self).delete(*args, **kwargs)
