from .models import Brand, Model, Car
from modeltranslation.translator import TranslationOptions, register


@register(Brand)
class BrandTranslationOptions(TranslationOptions):
    fields = ('brand_name',)


@register(Model)
class ModelTranslationOptions(TranslationOptions):
    fields = ('model_name',)


@register(Car)
class CarTranslationOptions(TranslationOptions):
    fields = ('description', 'task',)
