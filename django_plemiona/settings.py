import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(dotenv_path=BASE_DIR / ".env")

DEBUG = os.environ["DEBUG"]

ALLOWED_HOSTS = os.environ["ALLOWED_HOSTS"].split(",")
# Should be string with commas, like "localhost:8000,localhost:3000"

SECRET_KEY = os.environ["SECRET_KEY"]

INSTALLED_APPS = [
    "base.apps.BaseConfig",
    "tribal_wars",
    "api.apps.ApiConfig",
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

ROOT_URLCONF = "django_plemiona.urls"

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

WSGI_APPLICATION = "django_plemiona.wsgi.application"

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
    ("* */2 * * *", "base.cron.db_update"),
    ("0 3 * * *", "base.cron.outdate_overviews_delete"),
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

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

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
RECAPTCHA_PUBLIC_KEY = os.environ["RECAPTCHA_PUBLIC_KEY"]
RECAPTCHA_PRIVATE_KEY = os.environ["RECAPTCHA_PRIVATE_KEY"]

SILENCED_SYSTEM_CHECKS = os.environ["SILENCED_SYSTEM_CHECKS"].split(",")
