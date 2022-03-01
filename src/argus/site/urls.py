"""Argus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.decorators.csrf import csrf_exempt

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from social_django.urls import extra

from argus.auth.views import ObtainNewAuthToken, saml_metadata_view
from argus.dataporten import views as dataporten_views
from argus.site.views import error, MetadataView


extra = getattr(settings, "TRAILING_SLASH", True) and "/" or ""
psa_urls = [
    path("saml-metadata/", saml_metadata_view, name="social:saml-metadata"),
    re_path(fr"^complete/(?P<backend>saml){extra}$", csrf_exempt(dataporten_views.login_wrapper), name="complete"),
    # Overrides social_django's `complete` view
    # re_path(fr"^complete/(?P<backend>[^/]+){extra}$", dataporten_views.login_wrapper, name="complete"),
    path("", include("social_django.urls", namespace="social")),
]

urlpatterns = [
    # path(".error/", error),  # Only needed when testing error pages and error behavior
    path("admin/", admin.site.urls),
    path("oidc/", include(psa_urls)),
    path("api/schema/", SpectacularAPIView.as_view(api_version="v1"), name="schema-v1-old"),
    path("api/schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema-v1-old"), name="swagger-ui-v1-old"),
    path("api/v1/", include(("argus.site.api_v1_urls", "api"), namespace="v1")),
    path("api/v2/", include(("argus.site.api_v2_urls", "api"), namespace="v2")),
    path("api/", MetadataView.as_view(), name="metadata"),
]
