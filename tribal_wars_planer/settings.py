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

env_debug = os.environ["DEBUG"]
if env_debug in ["True", "true"]:
    DEBUG = True
else:
    DEBUG = False

ALLOWED_HOSTS = [os.environ["MAIN_DOMAIN"], os.environ["SUB_DOMAIN"]]

SECRET_KEY = os.environ["SECRET_KEY"]

ADMINS = [("admin", os.environ["DEFAULT_FROM_EMAIL"])]

INSTALLED_APPS = [
    "base",
    "rest_api",
    "utils",
    "crispy_forms",
    "markdownx",
    "django_registration",
    "django_crontab",
    "captcha",
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
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
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

STRIPE_PUBLISHABLE_KEY = os.environ["STRIPE_PUBLISHABLE_KEY"]
STRIPE_SECRET_KEY = os.environ["STRIPE_SECRET_KEY"]
STRIPE_ENDPOINT_SECRET = os.environ["STRIPE_ENDPOINT_SECRET"]
STRIPE_PAYMENTS = {
    30: os.environ["ONE_MONTH"],
    55: os.environ["TWO_MONTHS"],
    70: os.environ["THREE_MONTHS"],
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["POSTGRES_NAME"],
        "USER": os.environ["POSTGRES_USER"],
        "PASSWORD": os.environ["POSTGRES_PASSWORD"],
        "HOST": os.environ["POSTGRES_HOST"],
        "PORT": os.environ["POSTGRES_PORT"],
    }
}

CRONJOBS = [
    ("*/10 * * * *", "base.cron.db_update"),
    ("0 3 * * *", "base.cron.outdate_overviews_delete"),
    ("0 2 * * *", "base.cron.outdate_outline_delete"),
]

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

TIME_ZONE = "Europe/Warsaw"

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MARKDOWNX_MARKDOWNIFY_FUNCTION = "markdownx.utils.markdownify"
MARKDOWNX_MARKDOWN_EXTENSIONS = [
    "markdown.extensions.extra",
]
CRISPY_TEMPLATE_PACK = "bootstrap4"

LOGIN_REDIRECT_URL = "base:base"
LOGIN_URL = "login"
LOGOUT_REDIRECT_URL = "base:base"

EMAIL_BACKEND = os.environ["EMAIL_BACKEND"]
AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
AWS_SES_REGION_NAME = os.environ["AWS_SES_REGION_NAME"]
AWS_SES_REGION_ENDPOINT = os.environ["AWS_SES_REGION_ENDPOINT"]

DEFAULT_FROM_EMAIL = os.environ["DEFAULT_FROM_EMAIL"]
SERVER_EMAIL = os.environ["DEFAULT_FROM_EMAIL"]

RECAPTCHA_PUBLIC_KEY = os.environ["RECAPTCHA_PUBLIC_KEY"]
RECAPTCHA_PRIVATE_KEY = os.environ["RECAPTCHA_PRIVATE_KEY"]

SILENCED_SYSTEM_CHECKS = os.environ["SILENCED_SYSTEM_CHECKS"].split(",")
