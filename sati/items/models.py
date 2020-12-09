import os
import re
from pathlib import Path

from django.db import models
from django.utils.text import slugify

from .fields import ChoiceArrayField, CodingField


class UploadTo:
    def __init__(self, fieldname):
        self.fieldname = fieldname

    def __call__(self, instance, filename):
        folder = Path(instance.slug)
        max_length = instance._meta.get_field(self.fieldname).max_length

        # modified from django.utils.text.get_valid_filename
        filename = str(filename).strip().replace("/", "_")
        filename = re.sub(r"(?u)[^-\w.,]", "", filename)
        base, ext = os.path.splitext(filename)
        return folder / f"{base[: max_length - (len(folder.name) + len(ext) + 1)]}{ext}"

    # required to make this class serializable for migrations
    def deconstruct(self):
        return ("sati.items.models.UploadTo", [self.fieldname], {})


class ItemFormat(models.TextChoices):
    MC = "MC", "Multiple Choice"
    CR = "CR", "Constructed Response"
    FB = "FB", "Fill in the Blank"
    FT = "FT", "Fill in the Table/Chart/Graph"
    FI = "FI", "Fill in the Illustration"


class ItemLanguage(models.TextChoices):
    EN = "EN", "English"
    ZH = "ZH", "Chinese"


class ContentArea(models.TextChoices):
    EARTH_SCIENCE = "ES", "Earth Science"
    LIFE_SCIENCE = "LS", "Life Science"
    PHYSICAL_SCIENCE = "PS", "Physical Science"


class CodingScheme(models.TextChoices):
    WANG_2012 = "WC", "Wang, C. (2012)"


class ItemOrigin(models.Model):
    origin = models.JSONField()


class Item(models.Model):
    item_id = models.CharField(max_length=30, unique=True, verbose_name="Item ID")
    slug = models.SlugField(max_length=30, unique=True)
    name = models.CharField(max_length=30)
    language = models.CharField(
        max_length=2, choices=ItemLanguage.choices, verbose_name="Item Primary Language"
    )
    format = ChoiceArrayField(models.CharField(max_length=2, choices=ItemFormat.choices))
    content_area = models.CharField(
        max_length=2, choices=ContentArea.choices, verbose_name="Content Area"
    )
    main_image = models.ImageField(upload_to=UploadTo("main_image"), max_length=255)
    requires_attention = models.BooleanField(verbose_name="Requires Attention?")
    notes = models.TextField(blank=True, null=False, default="")
    ocr_text = models.TextField(blank=True, null=False, default="")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.item_id)
        super(Item, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.item_id} - {self.name.title()}"

    class Meta:
        ordering = ["id"]


class ItemCoding(models.Model):
    coding_source = models.CharField(max_length=30)
    coding_scheme = models.CharField(max_length=2, choices=CodingScheme.choices)
    coding = CodingField()
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return f"Coding from {self.coding_source}"
