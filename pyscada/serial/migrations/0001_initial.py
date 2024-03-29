# Generated by Django 2.2.8 on 2020-09-03 14:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("pyscada", "0059_auto_20200211_1049"),
    ]

    operations = [
        migrations.CreateModel(
            name="ExtendedSerialDevice",
            fields=[],
            options={
                "verbose_name": "Serial Device",
                "verbose_name_plural": "Serial Devices",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("pyscada.device",),
        ),
        migrations.CreateModel(
            name="ExtendedSerialVariable",
            fields=[],
            options={
                "verbose_name": "Serial Variable",
                "verbose_name_plural": "Serial Variables",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("pyscada.variable",),
        ),
        migrations.CreateModel(
            name="SerialVariable",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "serial_variable",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="pyscada.Variable",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SerialDevice",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "serial_device",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="pyscada.Device",
                    ),
                ),
            ],
        ),
    ]
