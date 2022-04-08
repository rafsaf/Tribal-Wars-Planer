# /bin/bash
echo "pushing docker twp-cronjobs image with tag $1"
docker build --platform linux/amd64,linux/arm64 . -f Dockerfile.cronjobs --tag rafsaf/twp-cronjobs:$1
docker image tag rafsaf/twp-cronjobs:$1 rafsaf/twp-cronjobs:$1
docker image push rafsaf/twp-cronjobs:$1