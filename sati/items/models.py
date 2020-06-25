import os
import re
from pathlib import Path

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.text import slugify

from .fields import ChoiceArrayField


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
    FB = "FB", "FB"
    FT = "FT", "FT"
    FI = "FI", "FI"


class ContentArea(models.TextChoices):
    EARTH_SCIENCE = "ES", "Earth Science"
    LIFE_SCIENCE = "LS", "Life Science"
    PHYSCIAL_SCIENCE = "PS", "Physical Science"


class CodingScheme(models.TextChoices):
    WANG = "WC", "Wang, C. (2012)"


class ItemOrigin(models.Model):
    origin = JSONField()


class Item(models.Model):
    item_id = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=30, unique=True)
    name = models.CharField(max_length=30)
    format = ChoiceArrayField(models.CharField(max_length=2, choices=ItemFormat.choices))
    content_area = models.CharField(max_length=2, choices=ContentArea.choices)
    main_image = models.ImageField(upload_to=UploadTo("main_image"), max_length=255)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.item_id)
        super(Item, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.item_id} - {self.name.title()}"


class ItemCoding(models.Model):
    coding_source = models.CharField(max_length=30)
    coding_scheme = models.CharField(max_length=2, choices=CodingScheme.choices)
    coding = JSONField()
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return f"Coding for {self.item}"
