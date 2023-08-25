#! /bin/bash

# Starts nginx + uwsgi server inside Dockerfile

### 1. Initial script, migrations etc., cleanup ###
bash /build/initial.sh

chown -R ${SERVICE_NAME}:${SERVICE_NAME} /build/logs
chown -R ${SERVICE_NAME}:${SERVICE_NAME} /build/media
chown -R ${SERVICE_NAME}:${SERVICE_NAME} /build/prometheus_multi_proc_dir
chown -R ${SERVICE_NAME}:${SERVICE_NAME} /build/disk_cache

### 2. Start uwsgi processes ### 
uwsgi --chdir=/build --uid=${SERVICE_NAME} --gid=${SERVICE_NAME} --module=tribal_wars_planer.wsgi:application --master --pidfile=/tmp/project-master.pid --socket=/tmp/uwsgi.sock --processes=${UWSGI_PROCESSES} --threads=${UWSGI_THREADS} --socket-timeout=150 --http-timeout=150 --harakiri=150 --home=/venv/ --daemonize=/build/logs/uwsgi.log

### 3. Start nginx ###
nginx -g "daemon off;"