#!/bin/bash

cd
sudo docker image prune --force
sudo docker compose stop web cronjobs
set +e
sudo docker compose pull && sudo docker compose up -d
sudo docker compose restart cronjobs
sudo docker image prune --force