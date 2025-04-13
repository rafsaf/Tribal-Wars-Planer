# Copyright 2021 Rafał Safin (rafsaf). All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
import os
import sys
import tomllib
from pathlib import Path
from typing import Any

from diskcache.fanout import FanoutCache
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

with open(BASE_DIR / "pyproject.toml", "rb") as f:
    pyproject_toml = tomllib.load(f)

BUILD_TAG = pyproject_toml["tool"]["poetry"]["version"]

load_dotenv(dotenv_path=BASE_DIR / ".env")

env_debug = os.environ.get("DEBUG", "false")
if env_debug in ["True", "true"]:
    DEBUG = True
else:
    DEBUG = False

TESTING = "pytest" in sys.modules
DEBUG_TOOLBAR = DEBUG and int(os.environ.get("DEBUG_TOOLBAR", "0")) == 1 and not TESTING
MAIN_DOMAIN = os.environ.get("MAIN_DOMAIN", "localhost")
SUB_DOMAIN = os.environ.get("SUB_DOMAIN", "")
ALLOWED_HOSTS = [MAIN_DOMAIN]
if SUB_DOMAIN:
    ALLOWED_HOSTS.append(SUB_DOMAIN)
if "localhost" not in ALLOWED_HOSTS:
    # docker image healthcheck require constantly requesting via localhost
    ALLOWED_HOSTS.append("localhost")
if "127.0.0.1" not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append("127.0.0.1")

INTERNAL_IPS = [
    "localhost",
    "127.0.0.1",
]

CSRF_TRUSTED_ORIGINS = os.environ.get(
    "CSRF_TRUSTED_ORIGINS", "http://localhost:8000,http://localhost:7999"
).split(",")

SECRET_KEY = os.environ["SECRET_KEY"]

DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "example@example.com")
SERVER_EMAIL = DEFAULT_FROM_EMAIL

JOB_MIN_INTERVAL = int(os.environ.get("JOB_MIN_INTERVAL", "10"))
JOB_MAX_INTERVAL = int(os.environ.get("JOB_MAX_INTERVAL", "15"))
WORLD_UPDATE_TRY_COUNT = int(os.environ.get("WORLD_UPDATE_TRY_COUNT", "1"))
WORLD_UPDATE_THREADS = int(os.environ.get("WORLD_UPDATE_THREADS", "1"))
env_world_update_fetch_all = os.environ.get("WORLD_UPDATE_FETCH_ALL", "false")
if env_world_update_fetch_all in ["True", "true"]:
    WORLD_UPDATE_FETCH_ALL = True
else:
    WORLD_UPDATE_FETCH_ALL = False

env_sentry_sdk_active = os.environ.get("SENTRY_SDK_ACTIVE", "false")
if env_sentry_sdk_active in ["True", "true"]:
    SENTRY_SDK_ACTIVE = True
else:
    SENTRY_SDK_ACTIVE = False

if SENTRY_SDK_ACTIVE:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        integrations=[DjangoIntegration()],
        dsn=os.environ["SENTRY_DSN"],
        server_name=MAIN_DOMAIN,
        environment=os.environ.get("SENTRY_ENVIRONMENT", "local"),
        release=BUILD_TAG,
        traces_sample_rate=float(os.environ.get("SENTRY_TRACES_SAMPLE_RATE", "1")),
    )

ADMINS = [("admin", DEFAULT_FROM_EMAIL)]

INSTALLED_APPS = [
    "base",
    "rest_api",
    "utils",
    "crispy_forms",
    "crispy_bootstrap4",
    "django_registration",
    "rest_framework",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_ses",
    "django_otp",
    "django_otp.plugins.otp_static",
    "django_otp.plugins.otp_totp",
    "django_otp.plugins.otp_email",
    "otp_yubikey",
    "two_factor",
    "two_factor.plugins.email",
    "two_factor.plugins.yubikey",
    "drf_spectacular",
]

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication"
    ],
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_THROTTLE_RATES": {"anon": "50/min", "user": "50/min"},
    "NUM_PROXIES": 2,
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Tribal Wars Planer API",
    "DESCRIPTION": "Tribal Wars Planer django app, professional tool for creating outlines for off-game coordinators.",
    "VERSION": BUILD_TAG,
    "SERVE_INCLUDE_SCHEMA": False,
    "EXTERNAL_DOCS": {"url": "https://plemiona-planer.pl/en/documentation/developers/"},
}

LOCALE_PATHS = [os.path.join(BASE_DIR, "locale")]

MIDDLEWARE = [
    "tribal_wars_planer.middlewares.PrometheusBeforeMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django_otp.middleware.OTPMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "tribal_wars_planer.middlewares.PrometheusAfterMiddleware",
]

if DEBUG_TOOLBAR:
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
    INSTALLED_APPS.append("debug_toolbar")

ROOT_URLCONF = "tribal_wars_planer.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "tribal_wars_planer.context_processors.build_tag",
            ],
        },
    },
]

WSGI_APPLICATION = "tribal_wars_planer.wsgi.application"

STRIPE_PUBLISHABLE_KEY = os.environ.get("STRIPE_PUBLISHABLE_KEY", "")
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "")
STRIPE_ENDPOINT_SECRET = os.environ.get("STRIPE_ENDPOINT_SECRET", "")

DATABASES: dict[str, dict[str, Any]] = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_NAME", "postgres"),
        "USER": os.environ.get("POSTGRES_USER", "postgres"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "postgres"),
        "HOST": os.environ.get("POSTGRES_HOST", "postgres"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
        "CONN_MAX_AGE": int(os.environ.get("CONN_MAX_AGE", "120")),
        "CONN_HEALTH_CHECKS": True,
    }
}

DATABASE_SSL_MODE_ON = os.environ.get("DATABASE_SSL_MODE_ON", "False")
if DATABASE_SSL_MODE_ON in ["True", "true"]:
    DATABASES["default"]["OPTIONS"] = {"sslmode": "require"}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


class PytestPBKDF2PasswordHasher(PBKDF2PasswordHasher):
    """
    A subclass of PBKDF2PasswordHasher that uses 1 iteration.
    """

    iterations = 1


if DEBUG and TESTING:
    PASSWORD_HASHERS = [
        "tribal_wars_planer.settings.PytestPBKDF2PasswordHasher",
    ]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en"
LANGUAGES = [
    ("en", "English"),
    ("pl", "Polish"),
]

LANGUAGE_COOKIE_AGE = 31104000
DATA_UPLOAD_MAX_MEMORY_SIZE = 20107200
TIME_ZONE = "Europe/Warsaw"

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage",
    },
}
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = "bootstrap4"

LOGIN_REDIRECT_URL = "base:base"
LOGIN_URL = "two_factor:login"
LOGOUT_REDIRECT_URL = "base:base"

EMAIL_BACKEND = os.environ.get(
    "EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend"
)
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
AWS_SES_REGION_NAME = os.environ.get("AWS_SES_REGION_NAME", "")
AWS_SES_REGION_ENDPOINT = os.environ.get("AWS_SES_REGION_ENDPOINT", "")
INPUT_OUTLINE_MAX_TARGETS = int(os.environ.get("INPUT_OUTLINE_MAX_TARGETS", "5000"))

TRIBALWARS_ANDROID_APP_NAME = "air.com.innogames.staemme"
METRICS_EXPORT_ENDPOINT_SECRET = os.environ.get(
    "METRICS_EXPORT_ENDPOINT_SECRET", "secret"
)

env_premium_acount_validation_on = os.environ.get(
    "PREMIUM_ACCOUNT_VALIDATION_ON", "false"
)
if env_premium_acount_validation_on in ["True", "true"]:
    PREMIUM_ACCOUNT_VALIDATION_ON = True
else:
    PREMIUM_ACCOUNT_VALIDATION_ON = False

PREMIUM_ACCOUNT_MAX_TARGETS_FREE = int(
    os.environ.get("PREMIUM_ACCOUNT_MAX_TARGETS_FREE", "25")
)

TRIBAL_WARS_SUPPORTED_SERVERS = [
    ("plemiona.pl", "pl", "Europe/Warsaw"),
    ("tribalwars.net", "en", "Europe/London"),
    ("die-staemme.de", "de", "Europe/Berlin"),
    ("staemme.ch", "ch", "Europe/Zurich"),
    ("tribalwars.nl", "nl", "Europe/Amsterdam"),
    ("tribalwars.com.br", "br", "America/Sao_Paulo"),
    ("tribalwars.com.pt", "pt", "Europe/Lisbon"),
    ("divokekmeny.cz", "cs", "Europe/Prague"),
    ("triburile.ro", "ro", "Europe/Bucharest"),
    ("voynaplemyon.com", "ru", "Europe/Moscow"),
    ("fyletikesmaxes.gr", "gr", "Europe/Athens"),
    ("divoke-kmene.sk", "sk", "Europe/Bratislava"),
    ("klanhaboru.hu", "hu", "Europe/Budapest"),
    ("tribals.it", "it", "Europe/Rome"),
    ("klanlar.org", "tr", "Europe/Istanbul"),
    ("guerretribale.fr", "fr", "Europe/Paris"),
    ("guerrastribales.es", "es", "Europe/Madrid"),
    ("tribalwars.ae", "ae", "Asia/Dubai"),
    ("tribalwars.co.uk", "uk", "Europe/London"),
    ("tribalwars.us", "us", "America/New_York"),
]

SUPPORTED_CURRENCIES = [
    "PLN",
    "EUR",
]

SUPPORTED_CURRENCIES_CHOICES = [
    (currency, currency) for currency in SUPPORTED_CURRENCIES
]

ACCOUNT_ACTIVATION_DAYS = 2
env_registration_open = os.environ.get("REGISTRATION_OPEN", "true")
if env_registration_open in ["False", "false"]:
    REGISTRATION_OPEN = False
else:
    REGISTRATION_OPEN = True

YUBICO_VALIDATION_SERVICE_API_ID = int(
    os.environ.get("YUBICO_VALIDATION_SERVICE_API_ID", "0")
)
YUBICO_VALIDATION_SERVICE_API_KEY = os.environ.get(
    "YUBICO_VALIDATION_SERVICE_API_KEY", ""
)

DJANGO_LOG_LEVEL = os.environ.get("DJANGO_LOG_LEVEL", "INFO")
DJANGO_LOG_HANDLERS = ["error", "info", "warning", "debug"]
if DJANGO_LOG_LEVEL == "DEBUG":
    DJANGO_LOG_HANDLERS.append("debug_stream")

os.makedirs("logs", exist_ok=True)
os.makedirs("prometheus_multi_proc_dir", exist_ok=True)
os.makedirs("media", exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{asctime} [{levelname}] {name}: {message}",
            "style": "{",
        },
        "simple": {
            "format": "{asctime}|{message}",
            "style": "{",
        },
    },
    "handlers": {
        "debug_stream": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
            "level": "DEBUG",
        },
        "error": {
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "logs/django_error.log",
            "formatter": "verbose",
            "level": "ERROR",
        },
        "warning": {
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "logs/django_warning.log",
            "formatter": "verbose",
            "level": "WARNING",
        },
        "info": {
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "logs/django_info.log",
            "formatter": "simple",
            "level": "INFO",
        },
        "debug": {
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "logs/django_debug.log",
            "formatter": "verbose",
            "level": "DEBUG",
        },
    },
    "loggers": {
        "": {
            "level": DJANGO_LOG_LEVEL,
            "handlers": DJANGO_LOG_HANDLERS,
            "propagate": False,
        },
    },
}

# disk cache im temp dir, 20gb limit
fanout_cache = FanoutCache(
    directory=BASE_DIR / "disk_cache", shards=20, timeout=1, size_limit=20 * 2**30
)

CACHES = {
    "default": {
        "BACKEND": "diskcache.DjangoCache",
        "LOCATION": str(BASE_DIR / "default_disk_cache"),
        "TIMEOUT": 300,
        # ^-- Django setting for default timeout of each key.
        "SHARDS": 8,
        "DATABASE_TIMEOUT": 0.010,  # 10 milliseconds
        # ^-- Timeout for each DjangoCache database transaction.
        "OPTIONS": {"size_limit": 2 * 2**30},  # 2 gigabyte
    },
}
