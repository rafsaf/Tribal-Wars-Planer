#!/bin/bash

cd ~/Tribal-Wars-Planer

sudo docker image prune --force
set +e
sudo docker-compose pull && sudo docker-compose up -d
sudo docker image prune --force