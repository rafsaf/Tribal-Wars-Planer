![plemiona-planer](https://plemiona-planer.pl/static/images/background.jpg)

# Official Site and Discord

[plemiona-planer.pl](https://plemiona-planer.pl/en/)

[discord.gg/g5pcsCteCT](https://discord.gg/g5pcsCteCT)

# Table of contents

[How to use this repo](#how-to-use-this-repo)

- [Quickstart](#quickstart)
- [Development](#development)
- [Test server](#test-server)

# How to use this repo

**Just need to have up and running [Docker](https://www.docker.com/get-started)**

If you want to run it in development and make use of `localhost:8000` (the quickstart app runs on `localhost:80`, you would need also:


- [python](https://www.python.org/downloads/) >= 3.9
- [poetry](https://python-poetry.org/)

## Quickstart

In your favourite folder e.g. Desktop:

```bash
git clone https://github.com/rafsaf/Tribal-Wars-Planer.git
cd Tribal-Wars-Planer

```
Go to the browser tab and write out `localhost`, enter


Then create file `.env` in Tribal-Wars-Planer from template file `.env.example`
Run

```bash
docker-compose up -d

```

Go to the browser tab and write out `localhost`, enter

## Development

> :warning: **No cron jobs will run in dev environment**!

In your favourite folder e.g. Desktop:

```bash
git clone https://github.com/rafsaf/Tribal-Wars-Planer.git
cd Tribal-Wars-Planer

```

Then create file `.env` in Tribal-Wars-Planer (you may overwrite defaults values for admin/secret keys) from template file `.env.example`

> :warning: Change `POSTGRES_HOST` to `localhost`.

Create venv inside root folder (for better linting in vs code) and install dependencies

```bash
# poetry config --list
# if virtualenvs.in-project = None or false, run
# poetry config virtualenvs.in-project true

poetry install

```

Run database with docker and then python

```bash
docker-compose -f docker-compose.dev.yml up -d
python mange.py migrate
python manage.py createsuperuser --no-input
python manage.py runserver
```

To run tests

```bash
python manage.py test
# python manage.py test base
# python manage.py test base.tests.test_views
```

To run makemessages/compilemessages

```bash
# linux only
python manage.py makemessages --all --ignore .venv

python manage.py compilemessages --ignore .venv
```

Test coverage

```bash
coverage run --source='.' --omit '.venv/*,*tests*,venv/*' manage.py test

coverage report
```

Running Stripe CLI on Windows (docker image)

```bash
# remember you need host.docker.internal as allowed host
# api-key is should be secret key from Stripe

docker run --rm -it stripe/stripe-cli:latest listen --forward-to host.docker.internal:8000/en/api/stripe-webhook/ --skip-verify --api-key sk_test_51IunwoIUoiUFYBGtpnRVBVro4iqXG8pndlUlpeBd1qbMNC9U7I0u6eQuCVjJdWMQoOpJhpyrztp2kUZSHMfi29Zh00TT5Q8yyL
```

## Test server

**Install Docker, docker-compose** eg.

```bash
sudo apt update
sudo apt upgrade
sudo apt install docker.io
sudo apt install docker-compose
sudo usermod -a -G docker ubuntu
# or other username than ubuntu
sudo reboot
# then log in again
docker info
# if ok, proceed
```

````
sudo ssh-keygen -t ed25519 -C "email@example.com"
sudo cat ~/.ssh/id_ed25519.pub

```bash
Copy and add to the:

Github.com -> Settings -> SSH and GPG keys

https://github.com/settings/keys

````

Finally clone repo

```bash
git clone git@github.com:rafsaf/Tribal-Wars-Planer.git
cd Tribal-Wars-Planer
cp .env.example .env
```

> :warning: SET DIFFRENT VALUES FOR:

```
DEBUG
MAIN_DOMAIN
SUB_DOMAIN
SECRET_KEY !!!!!!!!!!!!!
DEFAULT_FROM_EMAIL
POSTGRES_PASSWORD
DJANGO_SUPERUSER_PASSWORD !!!!!!!!!!!!!!!!!!!!!!! !!! !!! !!!!!!
```

**DO NOT LEAVE DJANGO_SUPERUSER_PASSWORD AS "ADMIN", SO ANYONE CAN LOGIN TO THE DASHBOARD**


```
docker-compose -f docker-compose.test.yml
```


