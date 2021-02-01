from unittest import TestCase

from django.urls.exceptions import Resolver404
from django.urls import resolve


NECESSARY_PATHS = (
    "/api/schema/",
    "/api/schema/swagger-ui/",
    "/api/v1/auth/logout/",
    "/api/v1/auth/phone-number/",
    "/api/v1/auth/phone-number/<pk>/",
    "/api/v1/auth/user/",
    "/api/v1/auth/users/<int:pk>/",
    "/api/v1/incidents/",
    "/api/v1/incidents/<int:incident_pk>/acks/",
    "/api/v1/incidents/<int:incident_pk>/acks/<int:pk>/",
    "/api/v1/incidents/<int:incident_pk>/events/",
    "/api/v1/incidents/<int:incident_pk>/events/<int:pk>/",
    "/api/v1/incidents/<pk>/",
    "/api/v1/incidents/<pk>/ticket_url/",
    "/api/v1/incidents/metadata/",
    "/api/v1/incidents/mine/",
    "/api/v1/incidents/open+unacked/",
    "/api/v1/incidents/open/",
    "/api/v1/incidents/source-types/",
    "/api/v1/incidents/source-types/<pk>/",
    "/api/v1/incidents/sources/",
    "/api/v1/incidents/sources/<pk>/",
    "/api/v1/notificationprofiles/",
    "/api/v1/notificationprofiles/<pk>/",
    "/api/v1/notificationprofiles/<pk>/incidents/",
    "/api/v1/notificationprofiles/filterpreview/",
    "/api/v1/notificationprofiles/filters/",
    "/api/v1/notificationprofiles/filters/<pk>/",
    "/api/v1/notificationprofiles/preview/",
    "/api/v1/notificationprofiles/timeslots/",
    "/api/v1/notificationprofiles/timeslots/<pk>/",
    "/api/v1/token-auth/",
)


class UrlsTest(TestCase):
    def test_no_necessary_paths_should_be_missing(self):
        missing = set()
        for path in NECESSARY_PATHS:
            try:
                resolve(path)
            except Resolver404:
                missing.add(path)
        self.assertFalse(missing)
