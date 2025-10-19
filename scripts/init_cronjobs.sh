#!/bin/bash
set -e

# Starts python schedule managed cronjobs inside Dockerfile

### 1. Cleanup and folder create ###
echo "prometheus multi proc directory, media creating and cleanup"
mkdir -p /build/prometheus_multi_proc_dir
mkdir -p /build/media
mkdir -p /build/logs
mkdir -p /build/disk_cache
mkdir -p /build/default_disk_cache

# Change ownership for proper permission handling
chmod 775 /build/logs
chown ${SERVICE_NAME}:root /build/logs
chown ${SERVICE_NAME}:${SERVICE_NAME} /build/media
chown ${SERVICE_NAME}:${SERVICE_NAME} /build/prometheus_multi_proc_dir
chown ${SERVICE_NAME}:${SERVICE_NAME} /build/disk_cache
chown ${SERVICE_NAME}:${SERVICE_NAME} /build/default_disk_cache

### 2. Run metrics on :8050 in the background
echo "start metrics thread"
runuser -u ${SERVICE_NAME} -- /usr/bin/nohup python scripts/expose_metrics_server.py &

### 3. Run init tasks ###

# admin user creation
username=${DJANGO_SUPERUSER_USERNAME} 
password=${DJANGO_SUPERUSER_PASSWORD}
email=${DJANGO_SUPERUSER_EMAIL}

echo "Creating first superuser, username:${username}, email:${email}"
export DJANGO_SUPERUSER_USERNAME=${username}
export DJANGO_SUPERUSER_PASSWORD=${password}
export DJANGO_SUPERUSER_EMAIL=${email}

runuser -u ${SERVICE_NAME} -- python manage.py createsuperuser --no-input || true

echo "initialize all supported servers"
runuser -u ${SERVICE_NAME} -- python manage.py createservers

echo "init stripe products and prices"
runuser -u ${SERVICE_NAME} -- python manage.py initstripe

echo "init 2fa"
runuser -u ${SERVICE_NAME} -- python manage.py init2fa

### 4. Run cronjobs ###

# runcronjobs specific environment variables
export CONN_MAX_AGE=0

echo "start cronjobs"
runuser -u ${SERVICE_NAME} -- python manage.py runcronjobs