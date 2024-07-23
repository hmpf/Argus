from argus.filter.filterwrapper import FilterBlobType
from argus.incident.models import Incident
from argus.notificationprofile.models import Filter
from argus.notificationprofile.models import NotificationProfile


def incidents_by_filter(incident_queryset, filter: Filter):
    "Returns all incidents that are included in the filter instance"
    return filtered_incidents(filter, incident_queryset).all()


def incidents_by_filter_pk(incident_queryset, filter_pk: int):
    """
    Returns all incidents that are included in the filter with the given primary
    key

    If no filter with that pk exists it returns no incidents
    """
    filtr = Filter.objects.filter(pk=filter_pk).first()

    if not filtr:
        return incident_queryset.none()

    return incidents_by_filter(incident_queryset, filtr)


def incidents_by_notificationprofile(incident_queryset, notificationprofile):
    filters = notificationprofile.filters.all()

    filtered_incidents_pks = set()
    for filtr in filters:
        filtered_incidents_pks.update(filtered_incidents(filtr, incident_queryset).values_list("pk", flat=True))

    return incident_queryset.filter(pk__in=filtered_incidents_pks)


def incidents_by_notificationprofile_pk(incident_queryset, notificationprofile_pk):
    """
    Returns all incidents that are included in the filters connected to the profile
    with the given primary key
    """
    notification_profile = NotificationProfile.objects.filter(pk=notificationprofile_pk).first()

    if not notification_profile:
        return incident_queryset.none()

    return incidents_by_notificationprofile(incident_queryset, notification_profile)


def _incidents_with_source_systems(incident_queryset, filterblob: FilterBlobType):
    source_list = filterblob.get("sourceSystemIds", [])
    if source_list:
        return incident_queryset.filter(source__in=source_list).distinct()
    return incident_queryset.distinct()


def _incidents_with_tags(incident_queryset, filterblob: FilterBlobType):
    tags_list = filterblob.get("tags", [])
    if tags_list:
        return incident_queryset.from_tags(*tags_list)
    return incident_queryset.distinct()


def _incidents_fitting_tristates(incident_queryset, filterblob: FilterBlobType):
    fitting_incidents = incident_queryset
    filter_open = filterblob.get("open", None)
    filter_acked = filterblob.get("acked", None)
    filter_stateful = filterblob.get("stateful", None)

    if filter_open is True:
        fitting_incidents = fitting_incidents.open()
    if filter_open is False:
        fitting_incidents = fitting_incidents.closed()
    if filter_acked is True:
        fitting_incidents = fitting_incidents.acked()
    if filter_acked is False:
        fitting_incidents = fitting_incidents.not_acked()
    if filter_stateful is True:
        fitting_incidents = fitting_incidents.stateful()
    if filter_stateful is False:
        fitting_incidents = fitting_incidents.stateless()
    return fitting_incidents.distinct()


def _incidents_fitting_maxlevel(incident_queryset, filterblob: FilterBlobType):
    maxlevel = filterblob.get("maxlevel", None)
    if not maxlevel:
        return incident_queryset.distinct()
    return incident_queryset.filter(level__lte=maxlevel).distinct()


def filtered_incidents(filter: Filter, incident_queryset=None):
    if incident_queryset is None:
        incident_queryset = Incident.objects.all()
    if filter.is_empty:
        return Incident.objects.none().distinct()
    filterblob = filter.filter.copy()
    filtered_by_source = _incidents_with_source_systems(incident_queryset, filterblob)
    filtered_by_tags = _incidents_with_tags(incident_queryset, filterblob)
    filtered_by_tristates = _incidents_fitting_tristates(incident_queryset, filterblob)
    filtered_by_maxlevel = _incidents_fitting_maxlevel(incident_queryset, filterblob)

    return filtered_by_source & filtered_by_tags & filtered_by_tristates & filtered_by_maxlevel
