import json
import re
from pathlib import Path

from django import forms
from django.conf import settings
from django.forms import CheckboxSelectMultiple
from django.utils.safestring import mark_safe
from django.utils.text import slugify


class ArraySelectMultiple(CheckboxSelectMultiple):
    def value_omitted_from_data(self, data, files, name):
        return False


class CodingWidget(forms.MultiWidget):
    template_name = "coding_widget.html"

    def __init__(self, attrs=None):
        super(CodingWidget, self).__init__([], attrs)

    def _get_dimensions(self, model_instance):
        self.dimensions = {}
        scheme = model_instance.get_coding_scheme_display()
        if not scheme:
            return
        dimensions_path = (
            Path(settings.BASE_DIR)
            / f"sati/items/schemas/{slugify(scheme)}_dimensions.json"
        )
        dimensions = json.load(dimensions_path.open())

        self.dimensions = {
            k: v for k, v in dimensions.items() if re.match(r"\d+\.\d+\.\d+", k)
        }

    def decompress(self, value):
        # Note: failing to implement this method causes a NotImplementedError to be
        # raised, but we're not actually using it...

        return [None] * len(self.dimensions)

    def value_from_datadict(self, data, files, name):
        boxes_checked = {
            key: value
            for (key, value) in data.items()
            if key.startswith(f"{name}_dimension")
        }
        self._get_dimensions(self.model_instance)
        return json.dumps(
            {
                dimension_id: int(f"{name}_dimension_{dimension_id}" in boxes_checked)
                for dimension_id in self.dimensions
            }
        )

    def render(self, name, value, attrs=None, renderer=None):
        coding = {}

        if value is not None and value != "null":
            coding = json.loads(value)

        self._get_dimensions(self.model_instance)

        widgets = {}
        for dimension_id, label in self.dimensions.items():
            widget_id = f"{name}_dimension_{dimension_id}"
            widget = forms.CheckboxInput(attrs={"id": widget_id})
            widgets[dimension_id] = {
                "id": widget_id,
                "html": widget.render(
                    widget_id, bool(coding.get(dimension_id, False)), widget.attrs,
                ),
                "dimension_id": dimension_id,
                "label": label,
            }

        attrs = {
            **attrs,
            **{
                "coding_scheme": self.model_instance.get_coding_scheme_display(),
                "dimensions": self.dimensions,
                "widgets": widgets,
            },
        }
        html = super().render(name, value, attrs)
        return mark_safe(html)
