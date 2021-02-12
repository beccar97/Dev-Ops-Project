# DevOps Apprenticeship: Project Exercise

[![Build Status](https://travis-ci.com/beccar97/Dev-Ops-Project.svg?branch=master)](https://travis-ci.com/beccar97/Dev-Ops-Project)

- [DevOps Apprenticeship: Project Exercise](#devops-apprenticeship-project-exercise)
  - [Getting started](#getting-started)
    - [Environment Variable setup](#environment-variable-setup)
    - [Mongo DB setup](#mongo-db-setup)
  - [Running the app using docker](#running-the-app-using-docker)
    - [Production](#production)
    - [Development](#development)
    - [Test](#test)
  - [Continuous Integration and Deployment](#continuous-integration-and-deployment)
  - [Virtual environment setup](#virtual-environment-setup)
    - [Running the project using vagrant](#running-the-project-using-vagrant)
      - [Running the tests within Vagrant](#running-the-tests-within-vagrant)
    - [Running the project locally using poetry](#running-the-project-locally-using-poetry)
      - [Running the app](#running-the-app)
      - [Running the tests using poetry](#running-the-tests-using-poetry)

## Getting started

### Environment Variable setup

To create the basic .env file for this project run

```bash
cp -n .env.template .env
```

from the project root directory. You will need to fill in values for the MongoDB related environment variables, as described below.

### Mongo DB setup

This project is set up to connect to a MongoDB cluster to store todo items. You will need to create a cluster authenticated with username and password, making note of these values. You will then need to update the .env file environment variables as follows:

- MONGO_USERNAME: Username for connecting to MongoDB cluser, can be see in the 'Database Access' menu under the 'Security' heading
- MONGO_PASSWORD: The password for the given user
- MONGO_URL: This is visible in the 'Connect' menu of your cluster, look for a url ending `.mongodb.net`
- MONGO_DEFAULT_DB: This is the name of the default database, it is set as 'todo_app' by default, but can be changed to any string you wish.

One option for setting up a MongoDB cluster is to use [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) which includes a free tier. Choosing "I'm learning MongoDB" option when signing up will give you very intuitive set-up instructions.

Note that Alas is IP restricted by default, you will need to change your cluster's Network Access settings to allow access from anywhere in order for your app to work correctly from within docker.

## Running the app using docker

There is a multi-stage docker file for this project, containing a production build and a development build:

### Production

- To produce the image: `docker build --target production --tag todo-app:prod .`
- To run: `docker run -p 5100:80 -e PORT=80 -d --env-file .env todo-app:prod`

The app will then run be accessible on localhost:5100.

### Development

The development container can be launched using `docker-compose up -d --build`. The app can then be accessed at localhost:5000 and will reload whenever changes are made to the app files locally.

 If you would prefer to build and run the image and container manually:

- To produce the image: `docker build --target development --tag todo-app:dev .`
- To run `docker run -p 5000:5000 -d --mount type=bind,source="$(pwd)",target=/app todo-app:dev`

### Test

- To produce the image: `docker build --target test --tag todo-app:test .`
- To run `docker run --mount type=bind,source="$(pwd)",target=/app todo-app:test`

## Continuous Integration and Deployment

Continuous integration and deployment is provided using Travis CI, specified in `.travis.yml`.
Tests are automatically run on any pull release branches, and the master branch is built and deployed to both docker hub and heroku. The heroku web app is released so it is always up to date with the current master. The live web app can be reached at [beccar-todo-app.herokuapp.com](https://beccar-todo-app.herokuapp.com/).

The Travis CI relies on several secure environment variables, which are defined by the `secure: <encoded environment variables>` line in the yml file. The encrypted key defining the variables is generated using the Travis CLI, as explained in [their documentation](https://docs.travis-ci.com/user/encryption-keys#usage). You can install the CLI using `gem install travis` and then to generate the encrypted key run the following (filling in the correct values for the environment variables).

```bash
travis encrypt --pro MONGO_URL=<MONGO_URL> \
MONGO_PASSWORD=<MONGO_PASSWORD> \
DOCKER_PASSWORD=<DOCKER_PASSSWORD> \
HEROKU_API_KEY=<HEROKU_API_KEY>
```

To get a heroku api key to use here follow the instructions in [this article](https://medium.com/@zulhhandyplast/how-to-create-a-non-expiring-heroku-token-for-daemons-ops-work-da08346286c0) to generate a non-expiring token. Note that the heroku account used will need to have the appropriate permissions to deploy the app.

In order for the app to run correctly when deployed, you will need to configure the production environment variables in Heroku. This can be done using commands such as

```bash
heroku config:set `cat .env | grep MONGO_USERNAME` --app <heroku_app_name>
```

You will need to configure the following environment variables for production:

- MONGO_USERNAME
- MONGO_PASSWORD
- MONGO_URL
- MONGO_DEFAULT_DB
- CREATE_VIRTUAL_ENV=true

Note, if any of these values are provided in quote marks in your .env file, then grep-ing them from there to set the heroku config will result in their values being saved with quote marks, which can cause errors.

If you wish to deploy to heroku locally for any reason you will need to login to the heroku container registry using the heroku CLI (see the [heroku documentation](https://devcenter.heroku.com/articles/container-registry-and-runtime#logging-in-to-the-registry)) and then run `./scripts/heroku_deploy_local.sh` from the root of the project.

## Virtual environment setup

The project uses a virtual environment to isolate package dependencies. The project uses poetry, and the virtual environment can be set up either locally or using Vagrant to run it on a virtual machine.

### Running the project using vagrant

In order to run the project using vagrant you must have installed a Hypervisor , VirtualBox is recommended. You must also download and install vagrant from the [official website](https://www.vagrantup.com/).

 To create the virtual environment and install required packages, run the following from a bash shell terminal, in the project root directory:

```bash
vagrant up
```

Running the `vagrant up` command will cause the app to run as a background process, visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

To stop the app running, destroy the virtual machine using

```bash
vagrant destroy
```

#### Running the tests within Vagrant

To run the tests when using Vagrant you must access the vagrant shell using

```bash
vagrant ssh
```

To run the tests navigate to the project directory by running

```bash
cd /vagrant
```

and then run the tests using

```bash
poetry run pytest
```

### Running the project locally using poetry

To run the project locally you must have poetry installed, installation instructions can be found at <https://pypi.org/project/poetry/>.

To create the virtual environment and install required packages, run the following from a bash shell terminal, in the project root directory:

```bash
poetry install
```

#### Running the app

Once the poetry install is complete, and the .env file set up, start the Flask app by running:

```bash
poetry run flask run
```

You should see output similar to the following:

```bash
 * Serving Flask app "src.app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```

Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

#### Running the tests using poetry

In order to run the tests you need to install the Chrome browser, and [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/). The chromedriver executable needs to be placed either in the project root directory, or in a location which is on your path.

Tests can be run from the command line by running:

```bash
poetry run pytest
```

If using VSCode can also set up to run tests from VSCode. In settings must set the following values:

```json
"python.testing.unittestEnabled": false
"python.testing.nosetestsEnabled": false
"python.testing.pytestEnabled": true
```

and then you can run 'Discover Tests' and 'Run Tests' from the command palette.

You will also need to correctly configure the python interpreter with VSCode. When running `poetry install` VSCode may prompt you to set the python interpreter, but if not run

```bash
poetry run which python
```

on a Mac/Linux, or

```powershell
poetry run where python
```

from Windows PowerShell to get the path to the python interpreter. Then in the bottom left of VSCode click the Python version in VSCode to bring up interpreter selection options, then point it at the virtual environment python executable.
