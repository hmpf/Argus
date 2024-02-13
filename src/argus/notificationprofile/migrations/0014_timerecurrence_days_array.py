# Generated by Django 4.1.7 on 2024-01-31 11:56

import django.contrib.postgres.fields
from django.db import migrations, models
from multiselectfield.db.fields import MultiSelectField

from argus.notificationprofile.models import TimeRecurrence


def copy_days_multiselectfield_to_days_array(apps, schema_editor):
    TimeRecurrence = apps.get_model("argus_notificationprofile", "TimeRecurrence")
    for t in TimeRecurrence.objects.all():
        t.days_array = [int(day) for day in t.days]
        t.save(update_fields=["days_array"])


def copy_days_array_to_days_multiselectfield(apps, schema_editor):
    TimeRecurrence = apps.get_model("argus_notificationprofile", "TimeRecurrence")
    for t in TimeRecurrence.objects.all():
        t.days = ",".join([str(day) for day in t.days_array])
        t.save(update_fields=["days"])


class Migration(migrations.Migration):
    dependencies = [
        ("argus_notificationprofile", "0013_remove_filter_filter_string"),
    ]

    operations = [
        migrations.AlterField(
            model_name="timerecurrence",
            name="days",
            field=MultiSelectField(choices=TimeRecurrence.Day.choices, min_choices=1, max_length=13, default="1"),
        ),
        migrations.AddField(
            model_name="timerecurrence",
            name="days_array",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.IntegerField(
                    choices=[
                        (1, "Monday"),
                        (2, "Tuesday"),
                        (3, "Wednesday"),
                        (4, "Thursday"),
                        (5, "Friday"),
                        (6, "Saturday"),
                        (7, "Sunday"),
                    ]
                ),
                default=[1],
                size=7,
            ),
            preserve_default=False,
        ),
        migrations.RunPython(copy_days_multiselectfield_to_days_array, copy_days_array_to_days_multiselectfield),
    ]