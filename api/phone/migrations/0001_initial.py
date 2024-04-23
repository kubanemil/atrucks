# Generated by Django 4.2.11 on 2024-04-23 11:16

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="PhoneInfo",
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
                ("abc_code", models.IntegerField()),
                ("min_code", models.IntegerField()),
                ("max_code", models.IntegerField()),
                ("operator", models.TextField()),
                ("region", models.TextField()),
            ],
        ),
        migrations.AddConstraint(
            model_name="phoneinfo",
            constraint=models.UniqueConstraint(
                fields=("abc_code", "min_code", "max_code"), name="unique_phone_info"
            ),
        ),
    ]