#!/bin/bash

# Starts python schedule managed cronjobs inside Dockerfile

### 1. Cleanup and folder create ###
echo "prometheus multi proc directory, media creating and cleanup"
mkdir prometheus_multi_proc_dir || true
mkdir media || true
mkdir logs || true
mkdir disk_cache || true
mkdir default_disk_cache || true

chown -R ${SERVICE_NAME}:${SERVICE_NAME} /build/logs
chown -R ${SERVICE_NAME}:${SERVICE_NAME} /build/media
chown -R ${SERVICE_NAME}:${SERVICE_NAME} /build/prometheus_multi_proc_dir
chown -R ${SERVICE_NAME}:${SERVICE_NAME} /build/disk_cache
chown -R ${SERVICE_NAME}:${SERVICE_NAME} /build/default_disk_cache

### 2. Run metrics on :8050 in the background
echo "start metrics thread"
runuser -u ${SERVICE_NAME} -- /usr/bin/nohup python scripts/expose_metrics_server.py &

### 3. Run cronjobs ###

# runcronjobs specific environment variables
export CONN_MAX_AGE=0

echo "start cronjobs"
runuser -u ${SERVICE_NAME} -- python manage.py runcronjobs