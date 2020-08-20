import json
from pathlib import Path

from jsonschema import validate, exceptions as jsonschema_exceptions

from django import forms
from django.conf import settings
from django.core import exceptions
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.fields import JSONField
from django.utils.text import slugify

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


class JSONSchemaField(JSONField):
    def __init__(self, *args, **kwargs):
        self.schema = kwargs.pop("schema", None)
        super().__init__(*args, **kwargs)

    @property
    def _schema_data(self):
        schema_path = Path(settings.BASE_DIR) / self.schema
        with schema_path.open("r") as _fh:
            return json.loads(_fh.read())

    def _validate_schema(self, value):
        # Disable validation when migrations are faked
        if self.model.__module__ == "__fake__":
            return True
        try:
            status = validate(value, self._schema_data)
        except jsonschema_exceptions.ValidationError as exp:
            raise exceptions.ValidationError(str(exp), code="invalid")
        return status

    def validate(self, value, model_instance):
        super().validate(value, model_instance)
        self._validate_schema(value)

    def pre_save(self, model_instance, add):
        value = super().pre_save(model_instance, add)
        if value and not self.null:
            self._validate_schema(value)
        return value


class CodingField(JSONSchemaField):
    """ This field inherits from JSONSchemaField (defined above in this module) and does
        one extra thing:
        1) it sets the schema for validation based on the value of
           `instance.coding_schema`.
    """

    def pre_save(self, model_instance, add):
        schema = model_instance.get_coding_scheme_display()
        self.schema = f"sati/items/schemas/{slugify(schema)}.json"
        value = super().pre_save(model_instance, add)
        return value
