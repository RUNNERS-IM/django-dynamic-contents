# Django
from django.db import models


# Class Section
class BaseModel(models.Model):

    # Basic
    title = models.TextField('제목', blank=True, null=True)

    # Dates
    created_at = models.DateTimeField('생성일자', auto_now_add=True, null=True)
    updated_at = models.DateTimeField('수정일자', auto_now=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return '{}({})'.format(self.title, self.id)


class ModelName(BaseModel):

    class Meta:
        verbose_name = 'model_name'
        verbose_name_plural = 'model_names'
        ordering = ['-created_at']
