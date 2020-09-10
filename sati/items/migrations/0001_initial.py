# Generated by Django 3.1.1 on 2020-09-10 05:58

from django.db import migrations, models
import django.db.models.deletion
import sati.items.fields
import sati.items.models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Item",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "item_id",
                    models.CharField(max_length=30, unique=True, verbose_name="Item ID"),
                ),
                ("slug", models.SlugField(max_length=30, unique=True)),
                ("name", models.CharField(max_length=30)),
                (
                    "format",
                    sati.items.fields.ChoiceArrayField(
                        base_field=models.CharField(
                            choices=[
                                ("MC", "Multiple Choice"),
                                ("CR", "Constructed Response"),
                                ("FB", "FB"),
                                ("FT", "FT"),
                                ("FI", "FI"),
                            ],
                            max_length=2,
                        ),
                        size=None,
                    ),
                ),
                (
                    "content_area",
                    models.CharField(
                        choices=[
                            ("ES", "Earth Science"),
                            ("LS", "Life Science"),
                            ("PS", "Physical Science"),
                        ],
                        max_length=2,
                        verbose_name="Content Area",
                    ),
                ),
                (
                    "main_image",
                    models.ImageField(
                        max_length=255,
                        upload_to=sati.items.models.UploadTo("main_image"),
                    ),
                ),
                (
                    "requires_attention",
                    models.BooleanField(verbose_name="Requires Attention?"),
                ),
                ("notes", models.TextField(blank=True, default="")),
            ],
            options={
                "ordering": ["id"],
            },
        ),
        migrations.CreateModel(
            name="ItemOrigin",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("origin", models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name="ItemCoding",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("coding_source", models.CharField(max_length=30)),
                (
                    "coding_scheme",
                    models.CharField(choices=[("WC", "Wang, C. (2012)")], max_length=2),
                ),
                ("coding", sati.items.fields.CodingField()),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="items.item"
                    ),
                ),
            ],
        ),
    ]