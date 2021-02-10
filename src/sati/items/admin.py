from django import forms
from django.contrib import admin
from django.db import models
from django.utils.safestring import mark_safe

from sati.items.models import Item, ItemCoding, ItemFormat, Test
from sati.items.fields import CodingField
from sati.users.models import User
from sati.widgets import AdminPagedownWidget


class ItemCodingForm(forms.ModelForm):
    coding = CodingField()

    class Meta:
        model = ItemCoding
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(ItemCodingForm, self).__init__(*args, **kwargs)

        # Pass the model instance in order to have access to the
        #  coding scheme in the CodingWidget.
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


class SubmittedByFilter(admin.SimpleListFilter):
    title = "Uploaded by"
    parameter_name = "submitted_by"

    def lookups(self, request, model_admin):
        return User.objects.exclude(item=None).values_list("uuid", "email")

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(submitted_by=self.value())
        return queryset


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    def _requires_attention(self, obj):
        alert = "<img src='/static/admin/img/icon-alert.svg' alt='Alert'>"
        if obj.requires_attention:
            return mark_safe(alert)
        return ""

    _requires_attention.admin_order_field = "requires_attention"
    _requires_attention.short_description = "Requires Attention?"

    def codings(self, obj):
        return obj.itemcoding_set.count()

    codings.short_description = "# Codings"

    save_on_top = True

    formfield_overrides = {
        models.TextField: {"widget": AdminPagedownWidget},
    }

    list_display = (
        "item_id",
        "name",
        "content_area",
        "format",
        "codings",
        "_requires_attention",
    )
    list_filter = (
        SubmittedByFilter,
        "requires_attention",
        "language",
        "content_area",
        ItemFormatFilter,
    )
    search_fields = ("item_id", "name", "ocr_text")

    inlines = [ItemCodingInline]

    fieldsets = (
        (
            "Item",
            {
                "fields": (
                    "item_id",
                    "name",
                    "test",
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

    def save_model(self, request, obj, form, change):
        if not change:
            obj.submitted_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["source_url"].widget.attrs["style"] = "width: 20em;"
        return form

    formfield_overrides = {
        models.TextField: {"widget": AdminPagedownWidget},
    }

    list_display = (
        "name",
        "year",
        "grade_level",
    )
