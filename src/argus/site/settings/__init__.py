from __future__ import annotations

import logging.config
from os import getenv
from pathlib import Path

from django.utils.module_loading import import_string


__all__ = [
    "SETTINGS_DIR",
    "SITE_DIR",
    "BASE_DIR",
    "get_bool_env",
    "get_str_env",
    "get_int_env",
    "get_str_from_file",
    "get_str_from_asciiarmorfile",
    "setup_logging",
    "update_loglevels",
]


# Build paths inside the project like this: BASE_DIR / ...
SETTINGS_DIR = Path(__file__).resolve().parent
SITE_DIR = SETTINGS_DIR.parent
BASE_DIR = SITE_DIR.parent


def get_any_env(envname, required=False):
    env = getenv(envname)
    if env is None:
        # Envvar not set!
        if required:
            error = f'Environment variable "{envname}" not set!'
            raise OSError(error)
        return None
    return env


def get_bool_env(envname, default=None, required=False):
    env = get_any_env(envname, required)
    env = str(env).lower()
    if env in {"1", "on", "true", "yes"}:
        return True
    if env in {"0", "off", "false", "no"}:
        return False
    return default


def get_str_env(envname, default="", required=False):
    env = get_any_env(envname, required)
    if env is None:
        return default
    return str(env).strip()


def get_int_env(envname, default=0, required=False):
    env = get_any_env(envname, required)
    if env is None:
        return default
    env = str(env).strip()
    return int(env)


def get_str_from_file(filename, encoding=None):
    with open(filename, encoding=encoding) as F:
        text = F.read()
    return text


def get_str_from_asciiarmorfile(filename, strip_armor=True):
    text = get_str_from_file(filename, encoding="ascii")
    if strip_armor:
        lines = [line.strip() for line in text.strip().split("\n")]
        prefixes_to_strip = ("-----BEGIN CERTIFICATE-----", "-----BEGIN PRIVATE KEY-----")
        if lines[0] in prefixes_to_strip:
            lines = lines[1:]
        suffixes_to_strip = ("-----END CERTIFICATE-----", "-----END PRIVATE KEY-----")
        if lines[-1] in suffixes_to_strip:
            lines = lines[:-1]
        text = "\n".join(lines)
    return text


def setup_logging(dotted_path=None):
    """Use the dictionary on the dotted path to set up logging

    Returns the dictionary on success, otherwise None.
    """
    if dotted_path:
        try:
            class_or_attr = import_string(dotted_path)
        except AttributeError:
            return
        logging.config.dictConfig(class_or_attr)
        return class_or_attr


def update_loglevels(loglevel: str = "INFO", loggers=(), handlers=()) -> None:
    """Override specific loglevels in already setup loggers or handlers"""
    loglevel = loglevel.upper()
    for logger in loggers:
        logging.getLogger(logger).setLevel(loglevel)
    if handlers:
        handlerdict = {}
        for handler in handlers:
            handlerdict["handler"] = {"level": loglevel}
        logdict = {"version": 1, "disable_existing_loggers": False, "incremental": True, "handlers": handlerdict}
        logging.config.dictConfig(logdict)
