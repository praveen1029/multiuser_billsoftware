# Generated by Django 4.2.3 on 2024-01-03 13:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("billapp", "0016_alter_item_itm_at_price_alter_item_itm_hsn_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transactions",
            name="item",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="billapp.item",
            ),
        ),
    ]