#!/bin/sh
echo 'Pushing to docker hub...'
docker push $DOCKER_USERNAME/$DOCKER_IMAGE_NAME:latest 
docker push $DOCKER_USERNAME/$DOCKER_IMAGE_NAME:$TRAVIS_COMMIT
echo 'Posting to Webhook...'
curl -dH -X POST "$(terraform output -raw webhook_url)"