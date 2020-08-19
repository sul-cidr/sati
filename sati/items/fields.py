from django import forms
from django.contrib.postgres.fields import ArrayField

from .widgets import ArraySelectMultiple


class ChoiceArrayField(ArrayField):
    def formfield(self, **kwargs):
        defaults = {
            "form_class": forms.TypedMultipleChoiceField,
            "choices": self.base_field.choices,
            "coerce": self.base_field.to_python,
            "widget": ArraySelectMultiple(attrs={"class": "choice-array-field"}),
        }
        defaults.update(kwargs)
        return super(ArrayField, self).formfield(**defaults)
