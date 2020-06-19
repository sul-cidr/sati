from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models


class ItemFormat(models.TextChoices):
    MC = "MC", "MC"
    CR = "CR", "CR"
    FB = "FB", "FB"
    FT = "FT", "FT"
    FI = "FI", "FI"


class ItemOrigin(models.Model):
    origin = JSONField()


class Item(models.Model):
    item_id = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=30)
    format = ArrayField(models.CharField(max_length=2, choices=ItemFormat.choices))
    # origin = models.ForeignKey(ItemOrigin, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.item_id} - {self.name.title()}"


class ItemCoding(models.Model):
    coding_source = models.CharField(max_length=30)
    coding_scheme = models.CharField(max_length=30)
    coding = JSONField()
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return f"Coding for {self.item}"
