from django.contrib import admin

from sati.items.models import Item, ItemCoding, ItemOrigin

admin.site.register(Item)
admin.site.register(ItemCoding)
admin.site.register(ItemOrigin)
