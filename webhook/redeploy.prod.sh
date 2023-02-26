#!/bin/bash

cd
rm -rf /var/lib/docker/volumes/root_twp_prd_prometheus/_data/*
rm -rf /var/lib/docker/volumes/root_twp_prd_logs/_data/*
sudo docker image prune --force
sudo docker compose start web2
echo "sleep 15..."
sleep 15
sudo docker compose stop web cronjobs
set +e
sudo docker compose pull && sudo docker compose up -d web
sudo docker compose restart web
echo "sleep 15"
sleep 15
sudo docker compose up -d web2
sudo docker compose stop web2
sudo docker compose restart cronjobs