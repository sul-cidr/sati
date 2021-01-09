from django import forms
from django.contrib import admin
from django.db import models

from sati.items.models import Item, ItemCoding, ItemFormat
from sati.items.fields import CodingField
from sati.widgets import AdminPagedownWidget


class ItemCodingForm(forms.ModelForm):
    coding = CodingField()

    class Meta:
        model = ItemCoding
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        """The model instance is passed here in order to have access to the coding
        scheme in the CodingWidget."""
        super(ItemCodingForm, self).__init__(*args, **kwargs)
        self.fields["coding"].widget.model_instance = self.instance
        self.fields["coding"].required = False


class ItemCodingInline(admin.StackedInline):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "submitted_by":
            kwargs["initial"] = request.user
            return db_field.formfield(**kwargs)
        return super(ItemCodingInline, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )

    form = ItemCodingForm
    model = ItemCoding
    extra = 0
    verbose_name = "Coding"
    verbose_name_plural = "Codings"


class ItemFormatFilter(admin.SimpleListFilter):
    title = "Format"
    parameter_name = "format"

    def lookups(self, request, model_admin):
        return ItemFormat.choices

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(format__contains=[self.value()])
        return queryset


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    save_on_top = True

    formfield_overrides = {
        models.TextField: {"widget": AdminPagedownWidget},
    }

    list_display = (
        "item_id",
        "name",
        "content_area",
        "format",
        "requires_attention",
    )
    list_filter = ("requires_attention", "language", "content_area", ItemFormatFilter)
    search_fields = ("item_id", "name", "ocr_text")

    inlines = [ItemCodingInline]

    fieldsets = (
        (
            "Item",
            {
                "fields": (
                    "item_id",
                    "name",
                    "language",
                    "content_area",
                    "format",
                    "requires_attention",
                    "notes",
                ),
                "classes": ("baton-tabs-init", "baton-tab-inline-itemcoding"),
            },
        ),
        ("Content", {"fields": ("main_image",)}),
    )

    list_per_page = 50
