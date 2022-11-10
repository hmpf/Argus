# Generated by Django 3.2.6 on 2022-03-11 15:24

from collections import defaultdict

from django.db import migrations, models


def copy_id_to_timeslot(apps, schema_editor):
    NotificationProfile = apps.get_model("argus_notificationprofile", "NotificationProfile")

    profiles = NotificationProfile.objects.all()
    for profile in profiles:
        profile.timeslot_id = profile.id

    NotificationProfile.objects.bulk_update(objs=profiles, fields=["timeslot"])


def fix_multi_use_timeslot_profiles(apps, schema_editor):
    Timeslot = apps.get_model("argus_notificationprofile", "Timeslot")
    TimeRecurrence = apps.get_model("argus_notificationprofile", "TimeRecurrence")

    timeslots = Timeslot.objects.prefetch_related("notification_profiles").annotate(
        num_profiles=models.Count("notification_profiles")
    )
    for timeslot in timeslots.filter(num_profiles__gt=1):
        profiles = timeslot.notification_profiles.order_by("pk").all()
        first_profile_id = profiles[0].id
        for i, profile in enumerate(profiles.exclude(id=first_profile_id)):
            new_timeslot, _ = Timeslot.objects.get_or_create(user=timeslot.user, name="".join([timeslot.name, str(i)]))
            for time_recurrence in timeslot.time_recurrences.all():
                new_time_recurrence, _ = TimeRecurrence.objects.get_or_create(
                    timeslot=new_timeslot,
                    days=time_recurrence.days,
                    start=time_recurrence.start,
                    end=time_recurrence.end,
                )
                new_timeslot.time_recurrences.add(new_time_recurrence)
            profile.timeslot_id = new_timeslot.id
            profile.save()


def copy_timeslot_to_id(apps, schema_editor):
    NotificationProfile = apps.get_model("argus_notificationprofile", "NotificationProfile")
    Filter = apps.get_model("argus_notificationprofile", "Filter")
    DestinationConfig = apps.get_model("argus_notificationprofile", "DestinationConfig")

    profiles = NotificationProfile.objects.exclude(id=models.F("timeslot_id"))
    filter_destination_copy = defaultdict(list)
    for profile in profiles:
        old_id = profile.id

        filters = tuple(profile.filters.values_list("id", flat=True))
        filter_destination_copy[profile.timeslot_id].append(filters)
        profile.filters.clear()

        destinations = tuple(profile.destinations.values_list("id", flat=True))
        filter_destination_copy[profile.timeslot_id].append(destinations)
        profile.destinations.clear()

        profile.id = profile.timeslot_id
        profile.save()

        # Delete old object
        NotificationProfile.objects.filter(id=old_id).exclude(id=models.F("timeslot_id")).delete()

    for pk, (filter_ids, destination_ids) in filter_destination_copy.items():
        try:
            profile = NotificationProfile.objects.get(id=pk)
        except NotificationProfile.DoesNotExist:
            continue
        profile.filters.set(Filter.objects.filter(id__in=filter_ids))
        profile.destinations.set(DestinationConfig.objects.filter(id__in=destination_ids))


class Migration(migrations.Migration):

    dependencies = [
        ("argus_notificationprofile", "0009_notificationprofile_id"),
    ]

    operations = [
        migrations.RunPython(migrations.RunPython.noop, copy_timeslot_to_id),
        migrations.RunPython(copy_id_to_timeslot, fix_multi_use_timeslot_profiles),
        migrations.AlterField(
            model_name="notificationprofile",
            name="timeslot",
            field=models.ForeignKey(
                on_delete=models.deletion.CASCADE,
                related_name="notification_profiles",
                to="argus_notificationprofile.timeslot",
            ),
        ),
        migrations.AddField(
            model_name="notificationprofile",
            name="name",
            field=models.CharField(
                blank=True,
                max_length=40,
                null=True,
            ),
        ),
        migrations.AddConstraint(
            model_name="notificationprofile",
            constraint=models.UniqueConstraint(fields=("user", "name"), name="unique_name_per_user"),
        ),
    ]