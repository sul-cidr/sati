from django.contrib import admin

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
    list_display = ("item_id", "name", "content_area", "format")
    list_filter = ("content_area", ItemFormatFilter)
    search_fields = ("item_id", "name")

    inlines = [ItemCodingInline]

    fieldsets = (
        (
            "Item",
            {
                "fields": ("item_id", "name", "content_area", "format"),
                "classes": ("baton-tabs-init", "baton-tab-inline-itemcoding"),
            },
        ),
    )

    list_per_page = 50
