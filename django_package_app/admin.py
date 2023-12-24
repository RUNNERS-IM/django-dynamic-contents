# vim: set fileencoding=utf-8 :
from django.contrib import admin, messages

# App
from django_package_app import models


# Main Section
class BaseModelAdmin(admin.ModelAdmin):
    actions = []


class ModelNameAdmin(BaseModelAdmin):
    list_display = ('title',)
    list_filter = ()


def _register(model, admin_class):
    admin.site.register(model, admin_class)


_register(models.ModelName, ModelNameAdmin)
