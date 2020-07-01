from django.contrib import admin
from django.db import models

from sati.widgets import AdminPagedownWidget
from sati.items.models import Item, ItemCoding, ItemFormat


class ItemCodingInline(admin.StackedInline):
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
    formfield_overrides = {
        models.TextField: {"widget": AdminPagedownWidget},
    }

    list_display = ("item_id", "name", "content_area", "format", "requires_attention")
    list_filter = ("requires_attention", "content_area", ItemFormatFilter)
    search_fields = ("item_id", "name")

    inlines = [ItemCodingInline]

    fieldsets = (
        (
            "Item",
            {
                "fields": (
                    "item_id",
                    "name",
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
