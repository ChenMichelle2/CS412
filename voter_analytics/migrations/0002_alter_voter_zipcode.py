# Generated by Django 5.1.1 on 2024-11-11 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("voter_analytics", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="voter",
            name="zipcode",
            field=models.IntegerField(),
        ),
    ]
