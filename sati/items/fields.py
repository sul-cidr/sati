import json
from pathlib import Path

from jsonschema import validate, exceptions as jsonschema_exceptions

from django import forms
from django.conf import settings
from django.core import exceptions
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.fields import JSONField

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
        1) it does some ugly dynamic work to set the schema for validation based on the
           value of instance.coding_schema (this should be redone at some point, in a
           better way).
    """

    def pre_save(self, model_instance, add):
        # This is all to get the member name from the Enum value
        # -- clearly this is not very good.
        from .models import CodingScheme

        schema = next(
            iter(
                k
                for k, v in CodingScheme.__members__.items()
                if v == model_instance.coding_scheme
            )
        )

        self.schema = f"sati/items/schemas/{schema.lower()}.json"
        value = super().pre_save(model_instance, add)
        return value
