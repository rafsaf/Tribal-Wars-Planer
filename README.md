![plemiona-planer](https://plemiona-planer.pl/static/images/background.jpg)

# Official Site and Discord

### Discord channel: [discord.gg/g5pcsCteCT](https://discord.gg/g5pcsCteCT)

### Production server: [plemiona-planer.pl](https://plemiona-planer.pl/en/)

Stage environment: [stg.plemiona-planer.pl](https://stg.plemiona-planer.pl/en/)

Test coverage 83%, see [Codecov raport](https://app.codecov.io/gh/rafsaf/Tribal-Wars-Planer)

# Table of contents

- [Quickstart: local usage](#quickstart)
- [Development](#development)
- [Test server](#test-server)

## Quickstart

**STEP 1**

Install [Docker](https://www.docker.com/get-started) on whatever system you work (On linux additionaly install docker-compose, on Windows and Mac it is included in docker installation)

**STEP 2**

In your favourite folder create file `docker-compose.yml`:

```yml
# docker-compose.yml
version: "3.3"

services:
  postgres:
    restart: always
    image: postgres
    volumes:
      - ./data_postgres/db:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=${POSTGRES_DB}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    env_file:
      - .env
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

  web:
    depends_on:
      - postgres
    restart: always
    image: rafsaf/twp-server:latest
    ports:
      - 7999:80
    env_file:
      - .env
    environment:
      - DEBUG=false
    volumes:
      - "./static/:/build/static/"

  cronjobs:
    depends_on:
      - postgres
    restart: always
    image: rafsaf/twp-cronjobs:latest
    env_file:
      - .env.example
    command: python -m base.run_cronjobs
    environment:
      - DJANGO_SETTINGS_MODULE=tribal_wars_planer.settings
```

Next step is to create `.env` file in the same folder with secrets. You can leave below settings "AS IS":

```bash
DEBUG=false
MAIN_DOMAIN=localhost
SUB_DOMAIN=
SECRET_KEY=your_secret_key
POSTGRES_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
# Set Email Backend to django_ses.SESBackend in production
# Above Development EMAIL_BACKEND would use terminal to send emails!
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_SES_REGION_NAME=
AWS_SES_REGION_ENDPOINT=
DEFAULT_FROM_EMAIL=example@example.com
# Below testing keys (always passing), do not use in production
RECAPTCHA_PUBLIC_KEY=6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI
RECAPTCHA_PRIVATE_KEY=6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe
# Set to empty in production
SILENCED_SYSTEM_CHECKS=captcha.recaptcha_test_key_error
# Default superuser
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=admin
DJANGO_SUPERUSER_EMAIL=admin@admin.com
STRIPE_PUBLISHABLE_KEY=
STRIPE_SECRET_KEY=
STRIPE_ENDPOINT_SECRET=
# Below put price_id for 30,55,70 PLN from Stripe account
ONE_MONTH=
TWO_MONTHS=
THREE_MONTHS=
METRICS_EXPORT_ENDPOINT_SECRET=secret
PROMETHEUS_MULTIPROC_DIR=prometheus_multi_proc_dir

```

Then run, (using Terminal in Linux/Mac, Powershell or CMD on Windows):

```bash
docker-compose up -d
# it may take up to few minutes
```

**STEP 3**

Go to the browser tab and write out `localhost:7999`, fresh instance of site should be up and running.

**STEP 4** (Login `admin`, Passwd `admin`)

You may see all declared variables in `.env.example` but login and password is `admin`, `admin`. The data will not be losed after reboot, it is docker volume (`data_postgres` folder in repository).

**STEP 5**

Activate premium account for admin (default) user you just logged in.

Go to `Administration` tab, then `Profiles` and choose `admin`, change "Validity date" to someting like 01.01.2100, just in case ;)

![image](./img/admin_profile.png)

**STEP 6**

Now you are free to create new worlds, and outlines just like in production server!

GL;)

## Development

If you want to run it in development and make use of `localhost:8000` (the quickstart app runs on `localhost:7999`, you would need also:

- [python](https://www.python.org/downloads/) >= 3.9
- [poetry](https://python-poetry.org/)

In your favourite folder e.g. Desktop:

```bash
git clone https://github.com/rafsaf/Tribal-Wars-Planer.git
cd Tribal-Wars-Planer

```

Then create file `.env` in Tribal-Wars-Planer from template file `.env.example`

> :warning: Change `POSTGRES_HOST` to `localhost`

Then run

```bash
poetry install

# it will be default create virtualenv in ~.cache/pypoetry/virutalenvs/tribal-wars-planer-asod(some random signs)
# You need to activate it.
# Honestly, you can also use just python3.9 -m venv .venv and run pip install -r requirements-dev.txt but above is prefered way
```

Run database with docker and then python dev server

```bash
docker-compose -f docker-compose.dev.yml up -d
# This set up db and cronjobs container
python manage.py migrate
python manage.py createsuperuser --no-input
# Default user will be admin (password admin), you may change this in .env file
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
docker compose -f docker-compose.translation.yml up -d

```

Test coverage

```bash
coverage run -m pytest
coverage report --show-missing
# Settings for coverage (also for other tools lives in pyproject.toml)
```

Running Stripe CLI on Windows (docker image)

```bash
# remember you need host.docker.internal as allowed host
# api-key is should be secret key from Stripe

docker run --rm -it stripe/stripe-cli:latest listen --forward-to host.docker.internal:8000/en/api/stripe-webhook/ --skip-verify --api-key sk_test_51IunwoIUoiUFYBGtpnRVBVro4iqXG8pndlUlpeBd1qbMNC9U7I0u6eQuCVjJdWMQoOpJhpyrztp2kUZSHMfi29Zh00TT5Q8yyL
```

## Server

On fresh ubuntu 20 webserver instance with enabled ports 9000, 443, 80 and sudo ports enabled:

```bash
sudo su && cd ~

wget https://raw.githubusercontent.com/rafsaf/Tribal-Wars-Planer/master/install_twp.sh \
  && bash install_twp.sh
# it will install all the boring stuff, refer to installation file

```

You can use printed webhook secret to trigger images pull and docker-compose up from anywhere:

```bash
curl -k -X POST https://$INSTANCE_IP:9000/hooks/redeploy \
  -H "Content-Type: application/json" -d '{"secret": "$SECRET"}'
```

Now in `/root/Tribal-Wars-Planer` folder, create `.env` and `docker-compose.yml` files:
Every environment variable is required!

```bash
# .env
DEBUG=false
MAIN_DOMAIN=example.com
SUB_DOMAIN=
SECRET_KEY=your_secret_key
POSTGRES_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres_password
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
# Set Email Backend to django_ses.SESBackend in production
# Above Development EMAIL_BACKEND would use terminal to send emails!
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_SES_REGION_NAME=
AWS_SES_REGION_ENDPOINT=
DEFAULT_FROM_EMAIL=example@example.com
# Below testing keys (always passing), do not use in production
RECAPTCHA_PUBLIC_KEY=6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI
RECAPTCHA_PRIVATE_KEY=6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe
# Set to empty in production
SILENCED_SYSTEM_CHECKS=captcha.recaptcha_test_key_error
# Default superuser
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=admin
DJANGO_SUPERUSER_EMAIL=admin@admin.com
STRIPE_PUBLISHABLE_KEY=
STRIPE_SECRET_KEY=
STRIPE_ENDPOINT_SECRET=
# Below put price_id for 30,55,70 PLN from Stripe account
ONE_MONTH=
TWO_MONTHS=
THREE_MONTHS=
METRICS_EXPORT_ENDPOINT_SECRET=secret
PROMETHEUS_MULTIPROC_DIR=prometheus_multi_proc_dir
```

```yml
# two domains, external database
version: "3.3"

services:
  web:
    restart: always
    image: rafsaf/twp-server:latest
    labels:
      - "traefik.enable=true"
      # static
      - "traefik.http.routers.web-static.rule=Host(`${MAIN_DOMAIN}`) && PathPrefix(`/static/`)"
      - "traefik.http.routers.web-static.entrypoints=websecure"
      - "traefik.http.routers.web-static.tls.certresolver=myresolver"
      - "traefik.http.middlewares.cache-headers.headers.customresponseheaders.Cache-Control=public,max-age=2592000"
      - "traefik.http.routers.web-static.middlewares=cache-headers"
      # default
      - "traefik.http.routers.web.rule=Host(`${MAIN_DOMAIN}`, `${SUB_DOMAIN}`)"
      - "traefik.http.routers.web.entrypoints=websecure"
      - "traefik.http.routers.web.tls.certresolver=myresolver"
      - "traefik.http.services.web.loadbalancer.server.port=80"
      # redirect domain to other
      - "traefik.http.middlewares.redirect-web.redirectregex.regex=^(https?://)${SUB_DOMAIN}/(.*)"
      - "traefik.http.middlewares.redirect-web.redirectregex.replacement=$${1}${MAIN_DOMAIN}/$${2}"
      - "traefik.http.middlewares.redirect-web.redirectregex.permanent=true"
      - "traefik.http.routers.web.middlewares=redirect-web"
    env_file:
      - .env
    environment:
      - DEBUG=false
    volumes:
      - "~/unit_log:/var/log"
      - "./media/:/build/media/"
      - "./static/:/build/static/"

  traefik:
    image: "traefik:v2.4"
    restart: always
    container_name: "traefik"
    command:
      # - "--log.level=DEBUG"
      - "--api.dashboard=false"
      - "--providers.docker=true"
      - "--providers.docker.exposedbydefault=false"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.websecure.address=:443"
      - "--entrypoints.web.http.redirections.entryPoint.to=websecure"
      - "--entrypoints.web.http.redirections.entryPoint.scheme=https"
      - "--certificatesresolvers.myresolver.acme.httpchallenge=true"
      - "--certificatesresolvers.myresolver.acme.httpchallenge.entrypoint=web"
      # test certificates
      # - "--certificatesresolvers.myresolver.acme.caserver=https://acme-staging-v02.api.letsencrypt.org/directory"
      - "--certificatesresolvers.myresolver.acme.email=${DEFAULT_FROM_EMAIL}"
      - "--certificatesresolvers.myresolver.acme.storage=/letsencrypt/acme.json"
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - "./letsencrypt:/letsencrypt"
      - "/var/run/docker.sock:/var/run/docker.sock:ro"

  cronjobs:
    restart: always
    image: rafsaf/twp-cronjobs:latest
    command: python -m base.run_cronjobs
    env_file:
      - .env
    environment:
      - DJANGO_SETTINGS_MODULE=tribal_wars_planer.settings
```

```yml
# one domain, internal database

version: "3.3"

services:
  postgres:
    restart: always
    image: postgres
    volumes:
      - ./data_test/db:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=${POSTGRES_DB}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    env_file:
      - .env
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

  web:
    depends_on:
      - postgres
    restart: always
    image: rafsaf/twp-server:latest
    labels:
      - "traefik.enable=true"
      # static
      - "traefik.http.routers.web-static.rule=Host(`${MAIN_DOMAIN}`) && PathPrefix(`/static/`)"
      - "traefik.http.routers.web-static.entrypoints=websecure"
      - "traefik.http.routers.web-static.tls.certresolver=myresolver"
      - "traefik.http.middlewares.cache-headers.headers.customresponseheaders.Cache-Control=public,max-age=2592000"
      - "traefik.http.routers.web-static.middlewares=cache-headers"
      # default
      - "traefik.http.routers.web.rule=Host(`${MAIN_DOMAIN}`)"
      - "traefik.http.routers.web.entrypoints=websecure"
      - "traefik.http.routers.web.tls.certresolver=myresolver"
      - "traefik.http.services.web.loadbalancer.server.port=80"
    env_file:
      - .env
    environment:
      - DEBUG=false
      - POSTGRES_HOST=postgres
    volumes:
      - "./media/:/build/media/"
      - "./static/:/build/static/"

  traefik:
    image: "traefik:v2.4"
    restart: always
    container_name: "traefik"
    command:
      # - "--log.level=DEBUG"
      - "--api.dashboard=false"
      - "--providers.docker=true"
      - "--providers.docker.exposedbydefault=false"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.websecure.address=:443"
      - "--entrypoints.web.http.redirections.entryPoint.to=websecure"
      - "--entrypoints.web.http.redirections.entryPoint.scheme=https"
      - "--certificatesresolvers.myresolver.acme.httpchallenge=true"
      - "--certificatesresolvers.myresolver.acme.httpchallenge.entrypoint=web"
      # test certificates
      # - "--certificatesresolvers.myresolver.acme.caserver=https://acme-staging-v02.api.letsencrypt.org/directory"
      - "--certificatesresolvers.myresolver.acme.email=${DEFAULT_FROM_EMAIL}"
      - "--certificatesresolvers.myresolver.acme.storage=/letsencrypt/acme.json"
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - "./letsencrypt:/letsencrypt"
      - "/var/run/docker.sock:/var/run/docker.sock:ro"

  cronjobs:
    restart: always
    image: rafsaf/twp-cronjobs:latest
    command: python -m base.run_cronjobs
    env_file:
      - .env
    environment:
      - DJANGO_SETTINGS_MODULE=tribal_wars_planer.settings
```

Just run

```
sudo docker-compose up -d
```

## Webhook playground

on fresh ubuntu

```bash
sudo apt-get install -y webhook
# test http
webhook -hooks /home/ubuntu/Tribal-Wars-Planer/webhook/hooks.json -verbose -hotreload
# test https
sudo openssl req -newkey rsa:4096 -keyout webhook.key -x509 -days 3650 -out webhook.crt -nodes
webhook -hooks /Tribal-Wars-Planer/webhook/hooks.json -verbose -hotreload -secure -cert /webhook.crt -key /webhook.key

# prod
# article
https://willbrowning.me/setting-up-automatic-deployment-and-builds-using-webhooks/

# commands
sudo apt install supervisor
cd /etc/supervisor/conf.d
sudo nano webhooks.conf

edit

[program:webhooks]
command=bash -c "/home/johndoe/go/bin/webhook -hooks /home/johndoe/hooks/hooks.json -verbose"
redirect_stderr=true
autostart=true
autorestart=true
user=johndoe
numprocs=1
process_name=%(program_name)s_%(process_num)s
stdout_logfile=/home/johndoe/hooks/supervisor.log
environment=HOME="/home/johndoe",USER="johndoe"

save and

touch ~/hooks/supervisor.log
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start webhooks:*
```
