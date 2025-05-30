"""
Django settings for Argus project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.2/ref/settings/
"""

import dj_database_url

# Import some helpers
from . import get_bool_env, get_str_env, get_int_env, setup_logging, get_json_env, validate_app_setting
from ..utils import update_settings

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = get_bool_env("DEBUG", False)

# Explicit is better than implicit!
ALLOWED_HOSTS = []
INTERNAL_IPS = []

# fmt: off
# fsck off, black
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # 3rd party apps
    "corsheaders",
    "social_django",
    "rest_framework",
    "rest_framework.authtoken",
    "drf_spectacular",
    "django_filters",
    "phonenumber_field",
    "knox",  # token auth

    # Argus apps
    "argus.auth",
    "argus.base",
    "argus.incident",
    "argus.filter",
    "argus.notificationprofile",
    "argus.dev",
]
# fmt: on

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "social_django.middleware.SocialAuthExceptionMiddleware",
    "django.contrib.auth.middleware.RemoteUserMiddleware",
]

ROOT_URLCONF = "argus.site.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "debug": get_bool_env("TEMPLATE_DEBUG", DEBUG),
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
            ],
        },
    }
]

WSGI_APPLICATION = "argus.site.wsgi.application"

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# fmt: off
DATABASE_URL = get_str_env("DATABASE_URL")
if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(DATABASE_URL),
    }
del DATABASE_URL
# fmt: on

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

AUTH_USER_MODEL = "argus_auth.User"

# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"

# Date formatting
DATE_FORMAT = "Y-m-d"
TIME_FORMAT = "H:i:s"
SHORT_TIME_FORMAT = "H:i"  # Not a Django setting
DATETIME_FORMAT = f"{DATE_FORMAT} {TIME_FORMAT}"
SHORT_DATETIME_FORMAT = f"{DATE_FORMAT} {SHORT_TIME_FORMAT}"

# Disable localized date and time formatting, due to the custom settings above
USE_L10N = False

USE_I18N = True

USE_TZ = True

TIME_ZONE = "Europe/Oslo"


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = get_str_env("STATIC_URL", "/static/")
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.RemoteUserBackend",
    "django.contrib.auth.backends.ModelBackend",
]

SILENCED_SYSTEM_CHECKS = [
    "rest_framework.W001",  # Turns off warning about PAGE_SIZE without DEFAULT_PAGINATION_CLASS
]


# Email

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_HOST = get_str_env("EMAIL_HOST", "localhost")
EMAIL_HOST_USER = get_str_env("EMAIL_HOST_USER")
EMAIL_PORT = get_int_env("EMAIL_PORT", 25)
EMAIL_USE_TLS = get_bool_env("EMAIL_USE_TLS", default=False)
EMAIL_HOST_PASSWORD = get_str_env("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = get_str_env("DEFAULT_FROM_EMAIL", "argus@localhost")

# Logging

LOGGING_MODULE = get_str_env("DJANGO_LOGGING_MODULE", None)
if LOGGING_MODULE:
    LOGGING_CONFIG = None
    STARTUP_LOGGING = setup_logging(LOGGING_MODULE)

# For permalinks to incidents in argus dashboard
FRONTEND_URL = get_str_env("ARGUS_FRONTEND_URL")

# django-rest-framework

# fmt: off
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "argus.auth.authentication.DeprecatedExpiringTokenAuthentication",
        "knox.auth.TokenAuthentication",
        # For BrowsableAPIRenderer
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        # Needs SessionAuthentication
        "rest_framework.renderers.BrowsableAPIRenderer",
    ),
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.NamespaceVersioning",
    "DEFAULT_VERSION": "v2",
    "EXCEPTION_HANDLER": "argus.drf.exception_handler",
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
    "PAGE_SIZE": 100,
}
# fmt: on

AUTH_TOKEN_EXPIRES_AFTER_DAYS = 14

# Project specific settings

# Set this to be able to send notifications
# MEDIA_PLUGINS = []

INDELIBLE_INCIDENTS = get_bool_env("ARGUS_INDELIBLE_INCIDENTS", True)

NOTIFICATION_SUBJECT_PREFIX = "[Argus] "

# Don't spam by accident
SEND_NOTIFICATIONS = get_bool_env("ARGUS_SEND_NOTIFICATIONS", default=False)

# 3rd party settings

# Python social auth

# Copied and adapted from social_core.pipeline.DEFAULT_AUTH_PIPELINE
# fmt: off
SOCIAL_AUTH_PIPELINE = (
    # Get the information we can about the user and return it in a simple
    # format to create the user instance later. In some cases the details are
    # already part of the auth response from the provider, but sometimes this
    # could hit a provider API.
    'social_core.pipeline.social_auth.social_details',

    # Get the social uid from whichever service we're authing thru. The uid is
    # the unique identifier of the given user in the provider.
    'social_core.pipeline.social_auth.social_uid',

    # Verifies that the current auth process is valid within the current
    # project, this is where emails and domains whitelists are applied (if
    # defined).
    'social_core.pipeline.social_auth.auth_allowed',

    # Checks if the current social-account is already associated in the site.
    'social_core.pipeline.social_auth.social_user',

    # Make up a username for this person, appends a random string at the end if
    # there's any collision.
    'social_core.pipeline.user.get_username',

    # Send a validation email to the user to verify its email address.
    # Disabled by default.
    # 'social_core.pipeline.mail.mail_validation',

    # Associates the current social details with another user account with
    # a similar email address. Disabled by default.
    # 'social_core.pipeline.social_auth.associate_by_email',

    # Create a user account if we haven't found one yet.
    'social_core.pipeline.user.create_user',

    # Create the record that associates the social account with the user.
    'social_core.pipeline.social_auth.associate_user',

    # Populate the extra_data field in the social record with the values
    # specified by settings (and the default ones like access_token, etc).
    'social_core.pipeline.social_auth.load_extra_data',

    # Update the user record with any changed info from the auth service.
    'social_core.pipeline.user.user_details',
)
# fmt: on

SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ["username", "first_name", "email"]
SOCIAL_AUTH_LOGIN_REDIRECT_URL = "/"
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = SOCIAL_AUTH_LOGIN_REDIRECT_URL

# Set these somewhere
# SOCIAL_AUTH_DATAPORTEN_KEY = get_str_env("ARGUS_DATAPORTEN_KEY", required=True)
# SOCIAL_AUTH_DATAPORTEN_SECRET = get_str_env("ARGUS_DATAPORTEN_SECRET", required=True)
#
# SOCIAL_AUTH_DATAPORTEN_EMAIL_KEY = SOCIAL_AUTH_DATAPORTEN_KEY
# SOCIAL_AUTH_DATAPORTEN_EMAIL_SECRET = SOCIAL_AUTH_DATAPORTEN_SECRET
#
# SOCIAL_AUTH_DATAPORTEN_FEIDE_KEY = SOCIAL_AUTH_DATAPORTEN_KEY
# SOCIAL_AUTH_DATAPORTEN_FEIDE_SECRET = SOCIAL_AUTH_DATAPORTEN_SECRET

# App settings: override themes, urls, context processors

# add apps that may override other apps
_overriding_apps_env = get_json_env("ARGUS_OVERRIDING_APPS", [], quiet=False)
OVERRIDING_APPS = validate_app_setting(_overriding_apps_env)
del _overriding_apps_env
update_settings(globals(), OVERRIDING_APPS, override=True)

# add extra functionality without overrides
_extra_apps_env = get_json_env("ARGUS_EXTRA_APPS", [], quiet=False)
EXTRA_APPS = validate_app_setting(_extra_apps_env)
del _extra_apps_env
update_settings(globals(), EXTRA_APPS)
