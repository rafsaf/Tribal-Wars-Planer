#!/bin/bash

cd /home/ubuntu/Tribal-Wars-Planer
git pull
docker image prune --force
docker-compose -f docker-compose.prod.yml up -d --build