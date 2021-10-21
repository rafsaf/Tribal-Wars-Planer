#!/bin/bash

cd /home/ubuntu/Tribal-Wars-Planer

git fetch
git reset --hard HEAD
git merge origin/master

docker image prune --force
set +e
docker-compose -f docker-compose.prod.yml up -d --build
docker image prune --force