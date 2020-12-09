#!/bin/sh
docker pull beckycarter/todo-app
docker tag beckycarter/todo-app registry.heroku.com/beccar-todo-app/web
docker push registry.heroku.com/beccar-todo-app/web
heroku container:release web --app beccar-todo-app
