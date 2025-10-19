#! /bin/bash
set -e

# Starts nginx + uwsgi server inside Dockerfile

### 1. App folders create, then migrations ###
echo "prometheus multi proc directory, media creating"

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

echo "staticfiles collection"
runuser -u ${SERVICE_NAME} -- python manage.py collectstatic --no-input

echo "migrations"
runuser -u ${SERVICE_NAME} -- python manage.py migrate

### 2. Run metrics on :8050 in the background
echo "start metrics thread"
runuser -u ${SERVICE_NAME} -- /usr/bin/nohup python scripts/expose_metrics_server.py &

### 3. Start uwsgi processes ### 
echo "start uwsgi"
uwsgi --chdir=/build --uid=${SERVICE_NAME} --gid=${SERVICE_NAME} \
    --module=tribal_wars_planer.wsgi:application --master --pidfile=/tmp/project-master.pid \
    --socket=/tmp/uwsgi.sock --processes=${UWSGI_PROCESSES} --threads=${UWSGI_THREADS} \
    --socket-timeout=360 --http-timeout=360 --harakiri=360 --home=/venv/ \
    --daemonize=/build/logs/uwsgi.log --ignore-sigpipe --ignore-write-errors --disable-write-exception

### 4. Start nginx ###
echo "start nginx"
nginx -g "daemon off;"