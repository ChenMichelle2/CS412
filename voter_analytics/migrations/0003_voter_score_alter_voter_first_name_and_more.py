# Generated by Django 5.1.1 on 2024-11-12 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("voter_analytics", "0002_alter_voter_zipcode"),
    ]

    operations = [
        migrations.AddField(
            model_name="voter",
            name="score",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="voter",
            name="first_name",
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name="voter",
            name="last_name",
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name="voter",
            name="street_name",
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name="voter",
            name="zipcode",
            field=models.CharField(max_length=50),
        ),
    ]
