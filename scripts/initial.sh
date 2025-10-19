#!/bin/bash
set -e

echo "prometheus multi proc directory, media creating"

mkdir -p prometheus_multi_proc_dir
mkdir -p media
mkdir -p logs
mkdir -p disk_cache
mkdir -p default_disk_cache

echo "staticfiles collection"
python manage.py collectstatic --no-input

echo "migrations"
python manage.py migrate

# default username and password admin, admin
username=${DJANGO_SUPERUSER_USERNAME:-admin} 
password=${DJANGO_SUPERUSER_PASSWORD:-admin}
email=${DJANGO_SUPERUSER_EMAIL:-admin@admin.com}

echo "Creating first superuser, username:${username}, email:${email}"
export DJANGO_SUPERUSER_USERNAME=${username}
export DJANGO_SUPERUSER_PASSWORD=${password}
export DJANGO_SUPERUSER_EMAIL=${email}

python manage.py createsuperuser --no-input || true

echo "initialize all supported servers"
python manage.py createservers

echo "init stripe products and prices"
python manage.py initstripe

echo "init 2fa"
python manage.py init2fa

