#!/bin/sh
chmod +x ./scripts/docker_entrypoint_prod.sh
echo 'Building production docker image...'
docker build --target production --cache-from $DOCKER_USERNAME/$DOCKER_IMAGE_NAME:latest --tag $DOCKER_USERNAME/$DOCKER_IMAGE_NAME:latest --tag $DOCKER_USERNAME/$DOCKER_IMAGE_NAME:$TRAVIS_COMMIT .
echo 'Pushing to docker hub...'
docker push $DOCKER_USERNAME/$DOCKER_IMAGE_NAME:latest 
docker push $DOCKER_USERNAME/$DOCKER_IMAGE_NAME:$TRAVIS_COMMIT
echo 'Posting to Webhook...'
echo "$(terraform output -raw webhook_url)"
echo $(terraform output -raw webhook_url)
curl -dH -X POST "$(terraform output -raw webhook_url)"