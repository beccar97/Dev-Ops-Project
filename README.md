# DevOps Apprenticeship: Project Exercise

[![Build Status](https://travis-ci.com/beccar97/Dev-Ops-Project.svg?branch=main)](https://travis-ci.com/beccar97/Dev-Ops-Project)

- [DevOps Apprenticeship: Project Exercise](#devops-apprenticeship-project-exercise)
  - [Getting started](#getting-started)
    - [Environment Variable setup](#environment-variable-setup)
    - [GitHub Auth setup](#github-auth-setup)
    - [Mongo DB setup](#mongo-db-setup)
  - [Running the app using docker](#running-the-app-using-docker)
    - [Production](#production)
      - [Troubleshooting](#troubleshooting)
    - [Development](#development)
    - [Test](#test)
  - [Continuous Integration and Deployment](#continuous-integration-and-deployment)
    - [Azure Service Principal](#azure-service-principal)
    - [Travis Environment Variable Configuration](#travis-environment-variable-configuration)
    - [Environment Variables in the App Service](#environment-variables-in-the-app-service)
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

from the project root directory. You will need to fill in values for several environment variables, as described below.

- FLASK_SECRET_KEY: Any GUID, used by Flask to sign session cookies
- For environments not using HTTPS add to the .env file `OAUTHLIB_INSECURE_TRANSPORT=1`
- The log level can be configured using the environment variable FLASK_LOG_LEVEL; if not set the log level will default to ERROR, note the .env.template file sets it to DEBUG as is designed for local use.

### GitHub Auth setup

This project uses GitHub Auth for authentication. If setting up with new app, follow the Github [documentation](https://developer.github.com/apps/building-oauth-apps/creating-an-oauth-app/) to create an OAuth app. For the homepage URL field enter the address for accessing the website locally. For the callback add a particular path to this URL for example `/login/callback`. Having created the app you will need the client id and secret, which should be entered into the .env file as the values of

- GITHUB_AUTH_CLIENT_ID
- GITHUB_AUTH_CLIENT_SECRET

respectively.

This OAuth app can then be used for running the project locally. In order for the production site (see [Continuous Integration and Deployment](#continuous-integration-and-deployment)) to work with OAuth you will need to create a second OAuth app using the production URL, and set up the production environment variables appropriately.

### Mongo DB setup

This project is set up to connect to a MongoDB cluster to store todo items. You will need to create a cluster authenticated with username and password, making note of these values.

The connection can either be configured using the username, password, url and default database individually, or by providing a connection string. Likely you will wish to use the former for local development and testing, and the latter in production.

If using a connection string, set the MONGO_CONNECTION_STRING variable in the .env file.

Otherwise update the .env file environment variables as follows:

- MONGO_USERNAME: Username for connecting to MongoDB cluser, can be see in the 'Database Access' menu under the 'Security' heading
- MONGO_PASSWORD: The password for the given user
- MONGO_URL: This is visible in the 'Connect' menu of your cluster, look for a url ending `.mongodb.net`
- MONGO_DEFAULT_DB: This is the name of the default database, it is set as 'todo_app' by default, but can be changed to any string you wish.

One option for setting up a MongoDB cluster is to use [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) which includes a free tier. Choosing "I'm learning MongoDB" option when signing up will give you very intuitive set-up instructions.

Note that Alas is IP restricted by default, you will need to change your cluster's Network Access settings to allow access from anywhere in order for your app to work correctly from within docker.

For a production setup recommend using Azure's Cosmos DB and providing the connection string to the app.

## Running the app using docker

There is a multi-stage docker file for this project, containing a production build and a development build:

### Production

- To produce the image: `docker build --target production --tag todo-app:prod .`
- To run: `docker run -p 5000:80 -e PORT=80 -d --env-file .env todo-app:prod`

The app will then run be accessible on localhost:5000. Note this cannot be run at the same time as the development version of the project, as they run on the same port. This is necessary for the Github auth redirection.

#### Troubleshooting

If when running the production image locally it fails to run, and you get the error `standard_init_linux.go:211: exec user process caused "no such file or directory"` the entrypoint script may have windows style line endings, causing issues. Run `dos2unix ./scripts/docker_entrypoint_prod.sh` from the project root and rebuild.

### Development

The development container can be launched using `docker-compose up -d --build`. The app can then be accessed at localhost:5000 and will reload whenever changes are made to the app files locally.

 If you would prefer to build and run the image and container manually:

- To produce the image: `docker build --target development --tag todo-app:dev .`
- To run `docker run -p 5000:5000 -d --mount type=bind,source="$(pwd)",target=/app todo-app:dev`

### Test

- To produce the image: `docker build --target test --tag todo-app:test .`
- To run `docker run --mount type=bind,source="$(pwd)",target=/app todo-app:test`

## Continuous Integration and Deployment

Continuous integration and deployment is provided using Travis CI, specified in `.travis.yml`. The CI is designed around the app being hosted in Azure, using a serverless CosmosDB database and an App Service for the main site. The infrastructure for the app is defined in main.tf.

Tests are automatically run on any pull release branches, and the main branch is deployed to the production system.

### Azure Service Principal

In order for Travis to access and alter Azure resources, a Service Principal is required, one can be created through the CLI using the following command:

```bash
$ az ad sp create-for-rbac --role="Contributor" -n name_for_principal
{
  "appId": SERVICE_PRINCIPAL_APP_ID,
  "displayName": NAME_FOR_PRINCIPAL,
  "name": "http://name_for_principal",
  "password" SERVICE_PRINCIPAL_PASSWORD,
  "tenant": SERVICE_PRINCIPAL_TENANT_ID
}
```

Note the values output by this command will be needed as environment variables to Travis, so should be saved somewhere secure.

### Travis Environment Variable Configuration

Travis requires many environment variables to be set, some which can be entered plainly into the .travis.yml file, and other secure environment variables which are defined by the `secure: <encoded environment variables>` lines in the yml file. The encrypted key defining the variables is generated using the Travis CLI, as explained in [their documentation](https://docs.travis-ci.com/user/encryption-keys#usage). You can install the CLI using `gem install travis` and then to generate the encrypted keys run the following,

- for the test stage:

```bash
travis encrypt --pro \
MONGO_URL=<MONGO_URL> \
MONGO_PASSWORD=<MONGO_PASSWORD> \
```

- for the release stage:

```bash
travis encrypt --pro \
DOCKER_PASSWORD=<DOCKER_PASSSWORD> \
ARM_CLIENT_ID=<SERVICE_PRINCIPAL_APP_ID> \
ARM_TENANT_ID=<SERVICE_PRINCIPAL_TENANT_ID> \
ARM_CLIENT_SECRET=<SERVICE_PRINCIPAL_PASSWORD> \
ARM_SUBSCRIPTION_ID=<SUBSCRIPTION_ID>
TF_VAR_github_auth_client_secret=<GITHUB_CLIENT_SECRET> \
TF_VAR_loggly_token=<LOGGLY_TOKEN>
```

- Environment variables with the prefix MONGO_ define the database connection used for running the selenium tests. Explanations of the individual variables can be found in [Mongo DB setup](#mongo-db-setup).
- Environment variables with the prefix TF_ are used by terraform, explanations can be found in [variables.tf](variables.tf)
- The values for ARM_CLIENT_ID, ARM_TENANT_ID, and ARM_CLIENT_SECRET all come from the output of creating the Service Principal ( see [Azure Service Principal](#azure-service-principal)).

### Environment Variables in the App Service

In order for the app to run correctly when deployed, you will need to configure the production environment variables in the Webapp.

This can be done using the portal, or via the CLI using `az webapp config appsettings set`. The file `azure_webapp_settings.json.template` provides a template json file which can be passed to this in order to load the variables at once.

You will need to configure the following environment variables for production:

- GITHUB_AUTH_CLIENT_ID
- GITHUB_AUTH_CLIENT_SECRET
- FLASK_SECRET_KEY
- MONGO_CONNECTION_STRING

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
