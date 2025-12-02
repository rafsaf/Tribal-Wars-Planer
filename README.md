![plemiona-planer](https://plemiona-planer.pl/static/images/background.avif)

![Codecov](https://img.shields.io/codecov/c/github/rafsaf/Tribal-Wars-Planer)
![GitHub](https://img.shields.io/github/license/rafsaf/Tribal-Wars-Planer)
![tests.yml](https://github.com/rafsaf/Tribal-Wars-Planer/actions/workflows/tests.yml/badge.svg)
![build_and_release.yml](https://github.com/rafsaf/Tribal-Wars-Planer/actions/workflows/build_and_release.yml/badge.svg)

# Official Site and Discord

### Discord channel: [discord.gg/g5pcsCteCT](https://discord.gg/g5pcsCteCT)

### Production server: [plemiona-planer.pl](https://plemiona-planer.pl)

Stage environment: [stg.plemiona-planer.pl](https://stg.plemiona-planer.pl)

Test coverage ~85%, see [Codecov raport](https://app.codecov.io/gh/rafsaf/Tribal-Wars-Planer)

# Table of contents

- [Official Site and Discord](#official-site-and-discord)
    - [Discord channel: discord.gg/g5pcsCteCT](#discord-channel-discordggg5pcsctect)
    - [Production server: plemiona-planer.pl](#production-server-plemiona-planerpl)
- [Table of contents](#table-of-contents)
- [Development](#development)
- [Dockerfile reference](#dockerfile-reference)
  - [TWP-server image](#twp-server-image)

# Development

If you want to run it in development you will need

- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [docker](https://www.docker.com/get-started)

In your favourite folder e.g. Desktop:

```bash
git clone https://github.com/rafsaf/Tribal-Wars-Planer.git
cd Tribal-Wars-Planer

```

Then create file `.env` in Tribal-Wars-Planer from template file `.env.example`

Then run

```bash
uv sync

# it will be default create virtualenv in .venv folder
# You need to activate it.
pre-commit install

# adds pre-commit stuff
```

Run database with docker and then python dev server

```bash
docker-compose up -d postgres_dev
# This set up db container

bash scripts/initial.sh
# migrations, creates admin/admin superuser, creates media and prometheus dirs, creates game servers

python manage.py runserver
# Runs development server at localhost:8000
```

To run tests with coverage report

```bash
pytest
```

To run makemessages/compilemessages (the project is in English, every string is then translated to Polish)

```bash
# every machine - using dockerfiles
docker compose -f docker-compose.translation.yml run --rm trans

```

# Dockerfile reference

This project maintains one docker images, the same one for server and for scheduling tasks. It's hosted via dockerhub and supports arm64 and amd64 architectures.

**NOTE, from 3.0.0 images support both linux/amd64 and linux/arm64 architectures.**

**NOTE, from 4.0.0 image twp-cronjobs is deprecated, please update for support. Cronjobs tasks are now runned from the main image.**

## TWP-server image

[TWP-server image on dockerhub](https://hub.docker.com/r/rafsaf/twp-server)

`rafsaf/twp-server:latest`

Note, there are also other tags like `stage` or `stable`, but **latest** should be prefered choice.

Contains TWP Django server based on `python:3.14` docker image, with [nginx](https://www.nginx.com/) + [uwsgi](https://uwsgi-docs.readthedocs.io/en/latest/) for webserver stack and tiny Python cron-like lib [schedule](https://schedule.readthedocs.io/en/stable/) for tasks and many more open source software.

Environment variables:

**SECRET_KEY** - _required_ - app secret key

**DEBUG** - _optional_ - debug boolean, defaults to `False`

**DJANGO_SUPERUSER_USERNAME** - _optional_ - first superuser username, defaults to `admin`

**DJANGO_SUPERUSER_PASSWORD** - _optional_ - first superuser password, defaults to `admin`

**DJANGO_SUPERUSER_EMAIL** - _optional_ - first superuser email, defaults to `admin@admin.com`

**MAIN_DOMAIN** - _optional_ - main domain used, defaults to `localhost`

**SUB_DOMAIN** - _optional_ - sub domain used, defaults to empty string

**CSRF_TRUSTED_ORIGINS** - _optional_ - list of domain that can perform POST and other unsafe requests to the app eg. `https://domain1,https://domain2,http://domain3`, see [django docs](https://docs.djangoproject.com/en/4.0/ref/settings/#std:setting-CSRF_TRUSTED_ORIGINS), defaults to `http://localhost:8000,http://localhost:7999`

**POSTGRES_NAME** - _optional_ - postgres database name, defaults to `postgres`

**POSTGRES_USER** - _optional_ - postgres database user, defaults to `postgres`

**POSTGRES_PASSWORD** - _optional_ - postgres database password, defaults to `postgres`

**POSTGRES_HOST** - _optional_ - postgres database host, defaults to `postgres`

**POSTGRES_PORT** - _optional_ - postgres database port, defaults to `5432`

**DATABASE_SSL_MODE_ON** - _optional_ - Require TLS/SSL when connecting to the database, defaults to `False`

**DEFAULT_FROM_EMAIL** - _optional_ - email of site owner, used to send emails on errors and certs expiration, defaults to `example@example.com`

**STRIPE_PUBLISHABLE_KEY** - _optional_ - stripe public key, defaults to empty string

**STRIPE_SECRET_KEY** - _optional_ - stripe secret key, defaults to empty string

**STRIPE_ENDPOINT_SECRET** - _optional_ - stripe endpoint, defaults to empty string

**EMAIL_BACKEND** - _optional_ - email backend, refer to django docs, defaults to `django.core.mail.backends.console.EmailBackend`

**AWS_ACCESS_KEY_ID** - _optional_ - AWS SES account key id, defaults to empty string

**AWS_SECRET_ACCESS_KEY** - _optional_ - AWS SES account secret, defaults to empty string

**AWS_SES_REGION_NAME** - _optional_ - AWS SES region, defaults to empty string

**AWS_SES_REGION_ENDPOINT** - _optional_ - AWS SES region endpoint, defaults to empty string

**METRICS_EXPORT_ENDPOINT_SECRET** - _optional_ - secret that allow (prometheus scrapers) access to `domain.com/api/metrics/?token=...`, defaults to `secret`

**UWSGI_PROCESSES** - _optional_ - number of uwsgi processes spawned in the container, defaults to 1

**PREMIUM_ACCOUNT_VALIDATION_ON** - _optional_ - is premium account required to create more targets, defaults to `False`

**PREMIUM_ACCOUNT_MAX_TARGETS_FREE** - _optional_ - max targets allowed without premium account, defaults to `25`

**REGISTRATION_OPEN** - _optional_ - is registration on site allowed, defaults to `True`

**JOB_LIFETIME_MAX_SECS** - _optional_ - Stops cronjob function after JOB_LIFETIME_MAX_SECS seconds, defaults to `0` and that means it will not stop ever. If number is greater than `0`, it must be also greater or equal to `120` (2 min).

**JOB_MIN_INTERVAL** - _optional_ - minimal time when database info about villages, players, worlds will be updated in minutes, defaults to `10`

**JOB_MAX_INTERVAL** - _optional_ - maximal time when database info about villages, players, worlds will be updated in minutes, defautls to `15`
