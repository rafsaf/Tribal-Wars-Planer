#!/bin/bash

cd
sudo docker image prune --force
sudo docker-compose start web2
sleep 30
set +e
sudo docker-compose pull && sudo docker-compose up -d web
sleep 30
sudo docker-compose up -d
sudo docker-compose stop web2