from modeltranslation.translator import translator, TranslationOptions
from .models import Format, Part, DynamicContent


# Class Section
class FormatTranslationOptions(TranslationOptions):
    fields = ('content',)


class PartTranslationOptions(TranslationOptions):
    fields = ('content',)


class DynamicContentTranslationOptions(TranslationOptions):
    fields = ('content',)


translator.register(Format, FormatTranslationOptions)
translator.register(Part, PartTranslationOptions)
translator.register(DynamicContent, DynamicContentTranslationOptions)