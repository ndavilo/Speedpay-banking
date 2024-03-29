# Generated by Django 4.1.4 on 2023-01-22 10:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0017_appussers"),
    ]

    operations = [
        migrations.CreateModel(
            name="AppUsers",
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
                ("username", models.CharField(max_length=100, unique=True)),
                ("password", models.CharField(max_length=100)),
                ("token", models.CharField(max_length=100)),
                (
                    "account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="app_account",
                        to="api.account",
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="AppUssers",
        ),
    ]
