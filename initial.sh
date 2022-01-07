#!/bin/bash

python manage.py collectstatic --no-input
python manage.py migrate
if [ -z ${var+DJANGO_SUPERUSER_USERNAME} ]; then export DJANGO_SUPERUSER_USERNAME=admin; else echo "username ok"; fi
if [ -z ${var+DJANGO_SUPERUSER_PASSWORD} ]; then export DJANGO_SUPERUSER_PASSWORD=admin; else echo "password ok"; fi
if [ -z ${var+DJANGO_SUPERUSER_EMAIL} ]; then export DJANGO_SUPERUSER_EMAIL=admin@admin.com; else echo "email ok"; fi
python manage.py createsuperuser --no-input
rm -rf prometheus_multi_proc_dir/*
