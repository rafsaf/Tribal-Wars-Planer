#!/bin/bash

echo "prometheus multi proc directory, media creating"

mkdir prometheus_multi_proc_dir || true
mkdir media || true
mkdir logs || true
mkdir disk_cache || true
mkdir default_disk_cache || true

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

python manage.py createsuperuser --no-input

echo "initialize all supported servers"
python manage.py createservers

echo "init stripe products and prices"
python manage.py initstripe

echo "init 2fa"
python manage.py init2fa

