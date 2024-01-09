from modeltranslation.translator import translator, TranslationOptions
from .models import Format, Part


class FormatTranslationOptions(TranslationOptions):
    fields = ('content',)


translator.register(Format, FormatTranslationOptions)
