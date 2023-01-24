# Generated by Django 4.1.4 on 2023-01-21 19:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0016_delete_appussers"),
    ]

    operations = [
        migrations.CreateModel(
            name="AppUssers",
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
                ("user_name", models.CharField(max_length=100, unique=True)),
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
    ]