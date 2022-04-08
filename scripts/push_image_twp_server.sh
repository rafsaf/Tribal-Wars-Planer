# /bin/bash
echo "pushing docker twp-server image with tag $1"
docker build --platform linux/amd64,linux/arm64 . -f Dockerfile.prod --tag rafsaf/twp-server:$1
docker image tag rafsaf/twp-server:$1 rafsaf/twp-server:$1
docker image push rafsaf/twp-server:$1