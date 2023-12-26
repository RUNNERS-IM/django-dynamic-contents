# vim: set fileencoding=utf-8 :
from django.contrib import admin

# App
from .models import Format, Part


# Main Section
class FormatAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'content', 'created_at', 'updated_at')
    search_fields = ('type', 'content')


class PartAdmin(admin.ModelAdmin):
    list_display = ('id', 'field', 'content', 'link', 'instance_id', 'created_at', 'updated_at')
    search_fields = ('field', 'content', 'instance_id')


class PartInline(admin.TabularInline):
    model = Part
    extra = 1  # 기본적으로 보여줄 빈 인라인 폼의 수


class DynamicContentAdminMixin:
    list_display = ('id', 'format', 'content_text', 'created_at', 'updated_at')
    search_fields = ('content_text',)
    inlines = [PartInline]
    list_filter = ('format',)


admin.site.register(Format, FormatAdmin)
admin.site.register(Part, PartAdmin)
