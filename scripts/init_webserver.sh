#! /bin/bash

# Starts nginx + uwsgi server inside Dockerfile.prod

### 1. Initial script, migrations etc., cleanup ###
bash /build/initial.sh

### 2. Start uwsgi processes ### 
uwsgi --chdir=/build --module=tribal_wars_planer.wsgi:application --master --pidfile=/tmp/project-master.pid --socket=/tmp/uwsgi.sock --processes=${UWSGI_PROCESSES} --harakiri=150 --max-requests=10000 --vacuum --home=/venv/ --daemonize=/build/logs/uwsgi.log

### 3. Start nginx ###
nginx -g "daemon off;"