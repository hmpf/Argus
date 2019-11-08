from datetime import datetime, time

from django.db import models
from django.utils import timezone
from multiselectfield import MultiSelectField

from aas.site.auth.models import User


class TimeSlotGroup(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'user'], name="unique_name_per_user"),
        ]
        ordering = ['name']

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='time_slot_groups',
    )
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class TimeSlot(models.Model):
    MONDAY = 'MO'
    TUESDAY = 'TU'
    WEDNESDAY = 'WE'
    THURSDAY = 'TH'
    FRIDAY = 'FR'
    SATURDAY = 'SA'
    SUNDAY = 'SU'
    DAY_CHOICES = (
        (MONDAY, "Monday"),
        (TUESDAY, "Tuesday"),
        (WEDNESDAY, "Wednesday"),
        (THURSDAY, "Thursday"),
        (FRIDAY, "Friday"),
        (SATURDAY, "Saturday"),
        (SUNDAY, "Sunday"),
    )
    group = models.ForeignKey(
        to=TimeSlotGroup,
        on_delete=models.CASCADE,
        related_name='time_slots',
    )

    day = models.CharField(max_length=2, choices=DAY_CHOICES)
    start = models.TimeField(help_text="Local time.")
    end = models.TimeField(help_text="Local time.")

    # TODO: replace these with making `start` and `end` custom timezone aware time fields
    #       (time+timezone is saved in database, to_python() returns custom time object that requires specifying a timezone
    #        - for comparison of objects)
    @property
    def utc_start(self):
        return self.local_time_to_utc_time(self.start)

    @property
    def utc_end(self):
        return self.local_time_to_utc_time(self.end)

    @staticmethod
    def local_time_to_utc_time(local_time: time):
        current_localtime = timezone.localtime()
        local_datetime = datetime.combine(current_localtime.date(), local_time, current_localtime.tzinfo)
        return local_datetime.astimezone(timezone.utc).time()

    def __str__(self):
        return f"{self.start}-{self.end} on {self.get_day_display()}s"


class Filter(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'user'], name="unique_name_per_user"),
        ]

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='filters',
    )
    name = models.CharField(max_length=40)
    filter_string = models.TextField()

    def __str__(self):
        return f"{self.name} [{self.filter_string}]"


class NotificationProfile(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='notification_profiles',
    )
    # TODO: add constraint that user must be the same
    time_slot_group = models.OneToOneField(
        to=TimeSlotGroup,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='notification_profile',
    )
    filters = models.ManyToManyField(
        to=Filter,
        related_name='notification_profiles',
    )

    EMAIL = 'EM'
    SMS = 'SM'
    SLACK = 'SL'
    MEDIA_CHOICES = (
        (EMAIL, "Email"),
        (SMS, "SMS"),
        (SLACK, "Slack"),
    )
    media = MultiSelectField(choices=MEDIA_CHOICES, min_choices=1, default=EMAIL)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.time_slot_group}: {', '.join(str(f) for f in self.filters.all())}"
