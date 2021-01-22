# Generated by Django 3.1.5 on 2021-01-16 00:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import sati.items.fields
import sati.items.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('item_id', models.CharField(max_length=30, unique=True, verbose_name='Item ID')),
                ('slug', models.SlugField(max_length=30, unique=True)),
                ('name', models.CharField(max_length=30)),
                ('language', models.CharField(choices=[('EN', 'English'), ('ZH', 'Chinese')], max_length=2, verbose_name='Item Primary Language')),
                ('format', sati.items.fields.ChoiceArrayField(base_field=models.CharField(choices=[('MC', 'Multiple Choice'), ('CR', 'Constructed Response'), ('FB', 'Fill in the Blank'), ('FT', 'Fill in the Table/Chart/Graph'), ('FI', 'Fill in the Illustration')], max_length=2), size=None)),
                ('content_area', models.CharField(choices=[('ES', 'Earth Science'), ('LS', 'Life Science'), ('PS', 'Physical Science')], max_length=2, verbose_name='Content Area')),
                ('main_image', models.ImageField(max_length=255, upload_to=sati.items.models.UploadTo('main_image'))),
                ('requires_attention', models.BooleanField(verbose_name='Requires Attention?')),
                ('notes', models.TextField(blank=True, default='')),
                ('ocr_text', models.TextField(blank=True, default='')),
                ('submitted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', related_query_name='item', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['item_id'],
            },
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('year', models.PositiveSmallIntegerField()),
                ('source_url', models.URLField(blank=True, default='', verbose_name='Source URL')),
                ('grade_level', models.PositiveSmallIntegerField(choices=[(0, 'Kindergarten'), (1, 'First Grade'), (2, 'Second Grade'), (3, 'Third Grade'), (4, 'Fourth Grade'), (5, 'Fifth Grade'), (6, 'Sixth Grade'), (7, 'Seventh Grade'), (8, 'Eighth Grade'), (9, 'Ninth Grade'), (10, 'Tenth Grade'), (11, 'Eleventh Grade'), (12, 'Twelfth Grade')], null=True, verbose_name='Grade Level')),
                ('notes', models.TextField(blank=True, default='')),
            ],
        ),
        migrations.CreateModel(
            name='ItemCoding',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('coding_scheme', models.CharField(choices=[('WC', 'Wang, C. (2012)')], default='WC', max_length=2)),
                ('coding', sati.items.fields.CodingField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='items.item')),
                ('submitted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itemcodings', related_query_name='itemcoding', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='item',
            name='test',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='items.test'),
        ),
    ]