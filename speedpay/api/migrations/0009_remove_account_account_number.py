# Generated by Django 4.1.4 on 2023-01-06 14:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0008_alter_account_id"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="account",
            name="account_number",
        ),
    ]
