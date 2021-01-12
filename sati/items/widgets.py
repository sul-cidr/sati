import json
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
    """This widget presents the JSON dict of coding dimensions in a nice layout
    according to the appropriate dimensions file found in sati/items/schemas/.
    It depends on self.model_instance to find the appropriate coding scheme --
    this is not normally available to a widget, but is passed in here from the
    custom ItemCodingForm defined in sati.items.admin which invokes the widget.
    """

    template_name = "coding_widget.html"

    def __init__(self, attrs=None):
        super(CodingWidget, self).__init__([], attrs)

    @staticmethod
    def _get_dimensions(model_instance):
        scheme = model_instance.get_coding_scheme_display()
        if not scheme:
            scheme = "Wang, C. (2012)"
        dimensions_path = (
            Path(settings.BASE_DIR)
            / f"sati/items/schemas/{slugify(scheme)}_dimensions.json"
        )
        return json.load(dimensions_path.open())

    def decompress(self, value):
        # Note: failing to implement this method causes a NotImplementedError to be
        # raised, even though we're not actually using it...

        return None

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["debug"] = settings.DEBUG
        return context

    def value_from_datadict(self, data, files, name):
        boxes_checked = {
            key: value
            for (key, value) in data.items()
            if key.startswith(f"{name}_dimension")
        }
        dimensions = self._get_dimensions(self.model_instance)
        dimension_ids = [
            dimension.split()[0]
            for section in dimensions.values()
            for subsection in section.values()
            for dimension in subsection
        ]

        return json.dumps(
            {
                dimension_id: int(f"{name}_dimension_{dimension_id}" in boxes_checked)
                for dimension_id in dimension_ids
            }
        )

    def render(self, name, value, attrs=None, renderer=None):
        coding = {}

        if value is not None and value != "null":
            coding = json.loads(value)

        dimensions = self._get_dimensions(self.model_instance)

        sections = {}
        for title, subsections in dimensions.items():
            _subsections = {}
            for subtitle, _dimensions in subsections.items():
                widgets = {}
                for dimension in _dimensions:
                    dimension_id, label, *_ = dimension.split(maxsplit=1) + [""]
                    widget_id = f"{name}_dimension_{dimension_id}"
                    widget = forms.CheckboxInput(attrs={"id": widget_id})
                    widgets[dimension_id] = {
                        "id": widget_id,
                        "html": widget.render(
                            widget_id,
                            bool(coding.get(dimension_id, False)),
                            widget.attrs,
                        ),
                        "dimension_id": dimension_id,
                        "label": label,
                    }

                _subsections[subtitle] = widgets
            sections[title] = _subsections

        attrs = {**attrs, **{"sections": sections}}
        html = super().render(name, value, attrs)
        return mark_safe(html)
