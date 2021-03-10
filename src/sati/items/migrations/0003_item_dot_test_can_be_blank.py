from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0002_itemcoding_notes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='test',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='items.test'),
        ),
    ]
