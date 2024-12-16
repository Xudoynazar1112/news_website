from modeltranslation.translator import register, TranslationOptions, translator
from .models import News, Category

@register(News)
class NewsTranslationOption(TranslationOptions):
    fields = ('title', 'body')
# 2-usul
# translator.register(News, TranslationOptions)

@register(Category)
class CategoryTranslationOption(TranslationOptions):
    fields = ('name',)

