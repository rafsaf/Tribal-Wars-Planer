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
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(dotenv_path=BASE_DIR / ".env")

env_debug = os.environ.get("DEBUG", False)
if env_debug in ["True", "true"]:
    DEBUG = True
else:
    DEBUG = False

ALLOWED_HOSTS = [
    os.environ.get("MAIN_DOMAIN", "localhost"),
    os.environ.get("SUB_DOMAIN", ""),
]
if "localhost" not in ALLOWED_HOSTS:
    # docker image healthcheck require constantly requesting via localhost
    ALLOWED_HOSTS.append("localhost")

CSRF_TRUSTED_ORIGINS = os.environ.get(
    "CSRF_TRUSTED_ORIGINS", "http://localhost:8000,http://localhost:7999"
).split(",")

SECRET_KEY = os.environ["SECRET_KEY"]

DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "example@example.com")
SERVER_EMAIL = DEFAULT_FROM_EMAIL

ADMINS = [("admin", DEFAULT_FROM_EMAIL)]

INSTALLED_APPS = [
    "base",
    "rest_api",
    "utils",
    "crispy_forms",
    "django_registration",
    "rest_framework",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication"
    ],
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
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
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "tribal_wars_planer.middlewares.PrometheusAfterMiddleware",
]

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
            ],
        },
    },
]

WSGI_APPLICATION = "tribal_wars_planer.wsgi.application"

STRIPE_PUBLISHABLE_KEY = os.environ.get("STRIPE_PUBLISHABLE_KEY", "")
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "")
STRIPE_ENDPOINT_SECRET = os.environ.get("STRIPE_ENDPOINT_SECRET", "")
STRIPE_PAYMENTS = {
    30: os.environ.get("ONE_MONTH", ""),
    55: os.environ.get("TWO_MONTHS", ""),
    70: os.environ.get("THREE_MONTHS", ""),
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_NAME", "postgres"),
        "USER": os.environ.get("POSTGRES_USER", "postgres"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "postgres"),
        "HOST": os.environ.get("POSTGRES_HOST", "postgres"),
        "PORT": os.environ.get("POSTGRES_PORT", 5432),
    }
}

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


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "pl"
LANGUAGES = [
    ("en", "English"),
    ("pl", "Polish"),
]

LANGUAGE_COOKIE_AGE = 31104000
DATA_UPLOAD_MAX_MEMORY_SIZE = 20107200
TIME_ZONE = "Europe/Warsaw"

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

CRISPY_TEMPLATE_PACK = "bootstrap4"

LOGIN_REDIRECT_URL = "base:base"
LOGIN_URL = "login"
LOGOUT_REDIRECT_URL = "base:base"

EMAIL_BACKEND = os.environ.get(
    "EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend"
)
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
AWS_SES_REGION_NAME = os.environ.get("AWS_SES_REGION_NAME", "")
AWS_SES_REGION_ENDPOINT = os.environ.get("AWS_SES_REGION_ENDPOINT", "")
INPUT_OUTLINE_MAX_TARGETS = int(os.environ.get("INPUT_OUTLINE_MAX_TARGETS", 5000))

METRICS_EXPORT_ENDPOINT_SECRET = os.environ.get(
    "METRICS_EXPORT_ENDPOINT_SECRET", "secret"
)

env_premium_acount_validation_on = os.environ.get(
    "PREMIUM_ACCOUNT_VALIDATION_ON", False
)
if env_premium_acount_validation_on in ["True", "true"]:
    PREMIUM_ACCOUNT_VALIDATION_ON = True
else:
    PREMIUM_ACCOUNT_VALIDATION_ON = False

PREMIUM_ACCOUNT_MAX_TARGETS_FREE = int(
    os.environ.get("PREMIUM_ACCOUNT_MAX_TARGETS_FREE", 25)
)

TRIBAL_WARS_SUPPORTED_SERVERS = [
    ("plemiona.pl", "pl"),
    ("tribalwars.net", "en"),
    ("die-staemme.de", "de"),
    ("staemme.ch", "ch"),
    ("tribalwars.nl", "nl"),
    ("tribalwars.com.br", "br"),
    ("tribalwars.com.pt", "pt"),
    ("divokekmeny.cz", "cz"),
    ("triburile.ro", "ro"),
    ("voyna-plemyon.ru", "ru"),
    ("fyletikesmaxes.gr", "gr"),
    ("divoke-kmene.sk", "sk"),
    ("klanhaboru.hu", "hu"),
    ("tribals.it", "it"),
    ("klanlar.org", "tr"),
    ("guerretribale.fr", "fr"),
    ("guerrastribales.es", "es"),
    ("tribalwars.ae", "ae"),
    ("tribalwars.co.uk", "uk"),
    ("tribalwars.us", "us"),
]

env_registration_open = os.environ.get("REGISTRATION_OPEN", True)
if env_registration_open in ["False", "false"]:
    REGISTRATION_OPEN = False
else:
    REGISTRATION_OPEN = True

DJANGO_LOG_LEVEL = os.environ.get("DJANGO_LOG_LEVEL", "WARNING")
os.makedirs("logs", exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{name} {levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "class": "logging.FileHandler",
            "filename": "logs/django.log",
            "formatter": "verbose",
            "level": DJANGO_LOG_LEVEL,
        },
    },
    "loggers": {
        "": {
            "level": DJANGO_LOG_LEVEL,
            "handlers": ["file"],
        },
    },
}
