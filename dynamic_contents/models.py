# Django
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

    type = models.CharField('Type (유형)', max_length=100, choices=[settings.DYNAMIC_CONTENT_CHOICES])
    content = models.TextField('Content (내용)')  # "{user}가 {post}를 좋아요합니다."

    class Meta:
        verbose_name = 'format'
        verbose_name_plural = 'formats'
        ordering = ['-created_at']


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


# Dynamic Content
class DynamicContentManager(models.Manager):

    def create_with_parts(self, format, parts_data):
        """
        주어진 포맷과 파트 데이터를 사용하여 DynamicContent와 연관된 Part 객체들을 생성합니다.

        :param format: DynamicContent의 Format 객체
        :param parts_data: Part 객체들에 대한 데이터 목록. 각 항목은 사전 형태로 되어 있어야 함.
        :return: 생성된 DynamicContent 객체
        """
        # DynamicContent 객체 생성
        dynamic_content = self.create(format=format)

        # Part 객체들 생성 및 연결
        for part_data in parts_data:
            part = Part.objects.create(**part_data)
            dynamic_content.parts.add(part)

        return dynamic_content


class DynamicContent(BaseModel):

    format = models.ForeignKey(Format, on_delete=models.CASCADE, related_name='contents')
    parts = models.ManyToManyField(Part, related_name='contents')

    content_text = models.TextField('Text Content', null=True, blank=True)
    content_html = models.TextField('Html Content', null=True, blank=True)

    class Meta:
        verbose_name = 'dynamic_content'
        verbose_name_plural = 'dynamic_contents'
        ordering = ['-created_at']

    def __str__(self):
        return '{}({})'.format(self.content)

    @property
    def text(self):
        format_string = self.format.content
        for part in self.parts.all():
            format_string = format_string.replace("{" + part.field + "}", part.content or '')
        if self.content_text != format_string:
            self.content_text = format_string
            self.save(update_fields=['content_text'])
        return self.content

    @property
    def html(self):
        format_string = self.format.content
        for part in self.parts.all():
            replacement = part.content or ''
            if part.link:
                replacement = f'<a href="{part.link}">{replacement}</a>'
            format_string = format_string.replace("{" + part.field + "}", replacement)
        return format_string
