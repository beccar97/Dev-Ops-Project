#!/bin/sh
chmod +x ./scripts/docker_entrypoint_prod.sh
echo 'Building production docker image...'
docker build --target production --cache-from $DOCKER_USERNAME/$DOCKER_IMAGE_NAME:latest --tag $DOCKER_USERNAME/$DOCKER_IMAGE_NAME:latest --tag $DOCKER_USERNAME/$DOCKER_IMAGE_NAME:$TRAVIS_COMMIT .
echo 'Pushing to docker hub...'
docker push $DOCKER_USERNAME/$DOCKER_IMAGE_NAME:latest 
docker push $DOCKER_USERNAME/$DOCKER_IMAGE_NAME:$TRAVIS_COMMIT
echo 'Posting to Webhook...'
curl -dH -X POST $WEBHOOK_URL