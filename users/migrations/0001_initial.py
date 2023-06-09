# Generated by Django 4.1.7 on 2023-03-21 18:03

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CustomUser",
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
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                ("email", models.EmailField(max_length=254, unique=True)),
                (
                    "first_name",
                    models.CharField(
                        blank=True, default=None, max_length=50, null=True
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, default=None, max_length=50, null=True
                    ),
                ),
                (
                    "phone_number",
                    models.CharField(
                        blank=True, default=None, max_length=20, null=True
                    ),
                ),
                ("cashback_point", models.IntegerField(default=0)),
                ("is_staff", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=False)),
                ("date_joined", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
