#!/bin/bash

echo "activate venv if exists (default folder venv inside docker image)"
if [ -d "venv" ]; then
  source venv/bin/activate || true
fi

echo "prometheus multi proc directory, media creating and cleanup"
mkdir prometheus_multi_proc_dir || true
mkdir media || true
mkdir logs || true
rm -rf prometheus_multi_proc_dir/*

echo "staticfiles collection"
python manage.py collectstatic --no-input

echo "migrations"
python manage.py migrate

echo "first superuser, by default admin, admin"
if [ -z ${var+DJANGO_SUPERUSER_USERNAME} ]; then export DJANGO_SUPERUSER_USERNAME=admin; else echo "username ok"; fi
if [ -z ${var+DJANGO_SUPERUSER_PASSWORD} ]; then export DJANGO_SUPERUSER_PASSWORD=admin; else echo "password ok"; fi
if [ -z ${var+DJANGO_SUPERUSER_EMAIL} ]; then export DJANGO_SUPERUSER_EMAIL=admin@admin.com; else echo "email ok"; fi
python manage.py createsuperuser --no-input

echo "initialize all supported servers"
python manage.py createservers

echo "init stripe products and prices"
python manage.py initstripe

