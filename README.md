![plemiona-planer](https://plemiona-planer.pl/static/images/background.jpg)

![Codecov](https://img.shields.io/codecov/c/github/rafsaf/Tribal-Wars-Planer)
![GitHub](https://img.shields.io/github/license/rafsaf/Tribal-Wars-Planer)
![tests](https://github.com/rafsaf/Tribal-Wars-Planer/actions/workflows/tests.yml/badge.svg)
![stage_image_push.yml](https://github.com/rafsaf/Tribal-Wars-Planer/actions/workflows/stage_image_push.yml/badge.svg)
![latest_image_push.yml](https://github.com/rafsaf/Tribal-Wars-Planer/actions/workflows/latest_image_push.yml/badge.svg)

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
- [Quickstart](#quickstart)
- [Dockerfile reference](#dockerfile-reference)
  - [TWP-server image](#twp-server-image)
- [Development](#development)
- [Server](#server)

# Quickstart

**STEP 1**

Install [Docker](https://www.docker.com/get-started) on whatever system you work (On linux additionaly install docker-compose, on Windows and Mac it is included in docker installation)

**STEP 2**

In your favourite folder create file `docker-compose.yml`. Too see every possible environemnt variables, see [Docker images reference](#dockerfile-reference):

```yml
# docker-compose.yml
version: "3.4"

services:
  postgres:
    restart: always
    image: postgres:15
    volumes:
      - twp_local_postgresql:/var/lib/postgresql/data
    environment:
      - POSTGRES_PASSWORD=postgres

  web:
    depends_on:
      - postgres
    restart: always
    image: rafsaf/twp-server:latest
    ports:
      - 7999:80
    environment:
      - SECRET_KEY=zaq12wsx3edc
      - DJANGO_SUPERUSER_USERNAME=admin
      - DJANGO_SUPERUSER_PASSWORD=admin
      - DJANGO_SUPERUSER_EMAIL=admin@admin.com

  cronjobs:
    depends_on:
      - postgres
    restart: always
    image: rafsaf/twp-server:latest
    command: bash /build/scripts/init_cronjobs.sh

volumes:
  twp_local_postgresql:
```

Then run, (using Terminal in Linux/Mac, Powershell or CMD on Windows):

```bash
docker-compose up -d
# it may take up to few minutes

# Note, if you see "ERROR 500" in app,
# it means that web container wasn't ready yet
# but should be good in another ~30 seconds
```

**STEP 3**

Go to the browser tab and write out `localhost:7999`, fresh instance of site should be up and running.

**STEP 4** (Login by default `admin` and password `admin`)

The database data will not be losed after reboot, it lives in docker volume folder.
For more details what exactly it means refer to Docker volumes docs.

**STEP 5**

Now you are free to create new worlds, and outlines just like in production server!

GL;)

# Dockerfile reference

This project maintains one docker images, the same one for server and for scheduling tasks. It's hosted via dockerhub and supports arm64 and amd64 architectures.

**NOTE, from 3.0.0 images support both linux/amd64 and linux/arm64 architectures.**

**NOTE, from 4.0.0 image twp-cronjobs is deprecated, please update for support. Cronjobs tasks are now runned from the main image.**

## TWP-server image

[TWP-server image on dockerhub](https://hub.docker.com/r/rafsaf/twp-server)

`rafsaf/twp-server:latest`

Note, there are also other tags like `stage` or `stable`, but **latest** should be prefered choice.

Contains TWP Django server based on `python:3.11.0-bullseye` docker image, with [nginx/1.18.0](https://www.nginx.com/) + [uwsgi](https://uwsgi-docs.readthedocs.io/en/latest/) for webserver stack and tiny Python cron-like lib [schedule](https://schedule.readthedocs.io/en/stable/) for tasks and many more open source software.

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

# Development

If you want to run it in development you will need

- [python](https://www.python.org/downloads/) == 3.11
- [poetry](https://python-poetry.org/)
- [docker](https://www.docker.com/get-started)

In your favourite folder e.g. Desktop:

```bash
git clone https://github.com/rafsaf/Tribal-Wars-Planer.git
cd Tribal-Wars-Planer

```

Then create file `.env` in Tribal-Wars-Planer from template file `.env.example`

Then run

```bash
poetry install

# it will be default create virtualenv in ~.cache/pypoetry/virutalenvs/tribal-wars-planer-asod(some random signs)
# You need to activate it.
# Honestly, you can also use just python3.11 -m venv .venv and run pip install -r requirements-dev.txt but above is prefered way
pre-commit install

# adds pre-commit stuff
```

Run database with docker and then python dev server

```bash
docker-compose -f docker-compose.dev.yml up -d
# This set up db and cronjobs container

bash initial.sh
# migrations, creates admin/admin superuser, creates media and prometheus dirs, creates game servers

python manage.py runserver
# Runs development server at localhost:8000
```

To run tests

```bash
pytest
# old way: python manage.py test
# python manage.py test base
# python manage.py test base.tests.test_views
```

To run makemessages/compilemessages (the project is in English, every string is then translated to Polish)

```bash
# every machine - using dockerfiles
docker compose -f docker-compose.translation.yml run --rm trans

```

Test coverage

```bash
coverage run -m pytest
coverage report --show-missing
# Settings for coverage (also for other tools lives in pyproject.toml)
```

# Server

On fresh ubuntu 20 webserver instance with enabled ports 9000, 443, 80 ports enabled and sudo access:

```bash
sudo su && cd

wget https://raw.githubusercontent.com/rafsaf/Tribal-Wars-Planer/master/scripts/install_twp.sh \
  && bash install_twp.sh
# it will install all the boring stuff, refer to installation file

```

You can use printed webhook secret to trigger images pull and docker-compose up from anywhere:

```bash
curl -v -k -X POST https://$INSTANCE_IP:9000/hooks/redeploy \
  -H "Content-Type: application/json" -d "{\"secret\": \"${SECRET}\"}"
```

Now in `~/` folder, create `.env` and `docker-compose.yml` files.

```bash
# .env
# ...see  Dockerfile reference
```

```yml
# two domains, external database or single domain with internal database
# ...see docker-compose.stg.yml or docker-compose.prod.yml
```

Then just run

```
sudo docker-compose up -d

```
