#! /bin/bash

# Starts nginx + uwsgi server inside Dockerfile

### 1. Initial script, migrations etc., cleanup ###
bash /build/scripts/initial.sh

chown -R ${SERVICE_NAME}:${SERVICE_NAME} /build/logs
chown -R ${SERVICE_NAME}:${SERVICE_NAME} /build/media
chown -R ${SERVICE_NAME}:${SERVICE_NAME} /build/prometheus_multi_proc_dir
chown -R ${SERVICE_NAME}:${SERVICE_NAME} /build/disk_cache

### 2. Run metrics on :8050 in the background
echo "start metrics thread"
runuser -u ${SERVICE_NAME} -- /usr/bin/nohup python scripts/expose_metrics_server.py &

### 3. Start uwsgi processes ### 
echo "start uwsgi"
uwsgi --chdir=/build --uid=${SERVICE_NAME} --gid=${SERVICE_NAME} --module=tribal_wars_planer.wsgi:application --master --pidfile=/tmp/project-master.pid --socket=/tmp/uwsgi.sock --processes=${UWSGI_PROCESSES} --threads=${UWSGI_THREADS} --socket-timeout=360 --http-timeout=360 --harakiri=360 --home=/venv/ --daemonize=/build/logs/uwsgi.log

### 3. Start nginx ###
echo "start nginx"
nginx -g "daemon off;"