# Generated by Django 4.1.4 on 2023-01-06 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0004_alter_account_account_number_alter_customer_email_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customer",
            name="phone_number",
            field=models.CharField(max_length=15),
        ),
    ]