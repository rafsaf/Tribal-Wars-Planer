from django_plemiona.settings import *

# make tests faster
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "postgres_github",
        "HOST": "127.0.0.1",
        "PORT": "5432",
    }
}
