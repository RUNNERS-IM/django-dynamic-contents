from modeltranslation.translator import translator, TranslationOptions
from .models import Format, Part


class FormatTranslationOptions(TranslationOptions):
    fields = ('content',)


class PartTranslationOptions(TranslationOptions):
    fields = ('content',)


translator.register(Format, FormatTranslationOptions)
translator.register(Part, PartTranslationOptions)
