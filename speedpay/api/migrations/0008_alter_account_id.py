# Generated by Django 4.1.4 on 2023-01-06 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0007_alter_account_account_number_alter_customer_email_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="account",
            name="id",
            field=models.IntegerField(
                editable=False, primary_key=True, serialize=False
            ),
        ),
    ]
