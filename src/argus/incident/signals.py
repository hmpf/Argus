from argus.notificationprofile.media import background_send_notifications_to_users
from .models import SourceSystem, Incident, Event, Acknowledgement


__all__ = [
    "delete_associated_user",
    "create_start_event",
    "send_notification",
    "delete_associated_event",
]


def delete_associated_user(sender, instance: SourceSystem, *args, **kwargs):
    if hasattr(instance, "user") and instance.user:
        instance.user.delete()


def create_start_event(sender, instance: Incident, created, raw, *args, **kwargs):
    if raw or not created:
        return
    if not instance.start_event:
        Event.objects.create(
            incident=instance,
            actor=instance.source.user,
            timestamp=instance.start_time,
            type=Event.Type.INCIDENT_START,
            description=instance.description,
        )


def send_notification(sender, instance: Event, *args, **kwargs):
    background_send_notifications_to_users(instance)


def delete_associated_event(sender, instance: Acknowledgement, *args, **kwargs):
    if hasattr(instance, "event") and instance.event:
        instance.event.delete()
