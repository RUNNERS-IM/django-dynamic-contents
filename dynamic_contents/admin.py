# vim: set fileencoding=utf-8 :
from django.conf import settings
from django.contrib import admin

# Third Party
from modeltranslation.admin import TranslationAdmin

# App
from .models import Format, Part


# Main Section
class FormatAdmin(TranslationAdmin):
    # 기본 list_display 설정
    list_display = ('id', 'type', 'subtype', 'content', 'created_at', 'updated_at')

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        # modeltranslation으로 생성된 번역 필드를 가져와서 list_display에 추가
        translated_fields = self.get_translated_fields()
        self.list_display = self.list_display + translated_fields

    def get_translated_fields(self):
        # 모델의 모든 필드를 순회하면서 번역 필드 확인
        translated_fields = []
        for field in self.model._meta.get_fields():
            if self.is_translated_field(field.name):
                translated_fields.append(field.name)
        return tuple(translated_fields)

    def is_translated_field(self, field_name):
        # 원래 필드명으로부터 생성된 번역 필드인지 확인
        return '_' in field_name and field_name.split('_')[-1] in dict(settings.LANGUAGES).keys()


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
