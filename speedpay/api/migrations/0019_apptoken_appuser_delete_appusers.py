# Generated by Django 4.1.4 on 2023-01-23 10:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0018_appusers_delete_appussers"),
    ]

    operations = [
        migrations.CreateModel(
            name="AppToken",
            fields=[
                ("dateTime", models.DateTimeField(auto_created=True)),
                (
                    "id",
                    models.IntegerField(
                        editable=False, primary_key=True, serialize=False
                    ),
                ),
                ("closed", models.BooleanField(default=False)),
                (
                    "account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="token_account",
                        to="api.account",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="AppUser",
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
                ("password", models.CharField(max_length=100)),
                ("varified", models.BooleanField(default=False)),
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
            name="AppUsers",
        ),
    ]
