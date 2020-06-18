from django.contrib.postgres.fields import JSONField
from django.db import models


class ItemCoding(models.Model):
    coding_source = models.CharField(max_length=30)
    coding_scheme = models.CharField(max_length=30)
    coding = JSONField()


class ItemOrigin(models.Model):
    item_id = models.CharField(max_length=30)
    other_ids = JSONField()
    origin = JSONField()


class Item(models.Model):
    origin = models.ForeignKey(ItemOrigin, on_delete=models.CASCADE)
