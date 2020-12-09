#!/bin/sh
chmod +x ./scripts/docker_entrypoint_prod.sh
echo 'Building production docker image...'
docker build --target production --tag $DOCKER_USERNAME/$DOCKER_IMAGE_NAME:latest --tag $DOCKER_USERNAME/$DOCKER_IMAGE_NAME:$TRAVIS_COMMIT .
echo 'Pushing to docker hub...'
docker push $DOCKER_USERNAME/$DOCKER_IMAGE_NAME:latest 
docker push $DOCKER_USERNAME/$DOCKER_IMAGE_NAME:$TRAVIS_COMMIT

echo 'Deploying to Heroku...'
docker tag $DOCKER_USERNAME/$DOCKER_IMAGE_NAME:latest registry.heroku.com/$HEROKU_APP_NAME/web
docker push registry.heroku.com/$HEROKU_APP_NAME/web
echo 'Releasing Heroku app..'
heroku container:release web --app $HEROKU_APP_NAME