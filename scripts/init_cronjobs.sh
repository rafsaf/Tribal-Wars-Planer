#!/bin/bash

# Starts python schedule managed cronjobs inside Dockerfile.prod

### 1. Cleanup and folder create ###
echo "prometheus multi proc directory, media creating and cleanup"
mkdir prometheus_multi_proc_dir || true
mkdir media || true
mkdir logs || true
rm -rf prometheus_multi_proc_dir/*

### 2. Run cronjobs ###
python manage.py runcronjobs