# Generated by Django 4.2.3 on 2024-01-03 06:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("billapp", "0014_remove_unitmodel_user_item_user_unitmodel_company_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Transactions",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("trans_type", models.CharField(max_length=255)),
                (
                    "trans_invoice",
                    models.PositiveBigIntegerField(blank=True, null=True),
                ),
                ("trans_name", models.CharField(max_length=255)),
                ("trans_date", models.DateTimeField()),
                ("trans_qty", models.PositiveBigIntegerField(default=0)),
                ("trans_current_qty", models.PositiveBigIntegerField(default=0)),
                ("trans_adjusted_qty", models.PositiveBigIntegerField(default=0)),
                ("trans_price", models.PositiveBigIntegerField(default=0)),
                ("trans_status", models.CharField(max_length=255)),
                (
                    "company",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="billapp.company",
                    ),
                ),
                (
                    "item",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="billapp.item",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.RenameModel(old_name="UnitModel", new_name="Unit",),
        migrations.DeleteModel(name="TransactionModel",),
    ]
