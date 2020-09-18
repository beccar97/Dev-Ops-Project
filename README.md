# DevOps Apprenticeship: Project Exercise

- [DevOps Apprenticeship: Project Exercise](#devops-apprenticeship-project-exercise)
  - [Getting started](#getting-started)
    - [Environment Variable setup](#environment-variable-setup)
    - [Trello setup](#trello-setup)
  - [Running the app using docker](#running-the-app-using-docker)
    - [Production:](#production)
    - [Development:](#development)
  - [Virtual environment setup](#virtual-environment-setup)
    - [Running the project using vagrant](#running-the-project-using-vagrant)
        - [Running the tests](#running-the-tests)
    - [Running the project locally using poetry](#running-the-project-locally-using-poetry)
      - [Running the app](#running-the-app)
      - [Running the tests](#running-the-tests-1)

## Getting started

### Environment Variable setup

To create the basic .env file for this project run 
```bash
$ cp -n .env.template .env
```
from the project root directory. You will need to fill in values for the trello related environment variables, as described below.

### Trello setup

In order to run the project you must link it to a Trello board. The app expects the board it is connected to to have three lists:
* To Do
* Doing
* Done

When you have created an appropriate trello board you need to add the board id to the .env file. The board id can be found from the URL of the board, the url has the format of `https://trello.com/b/<boardID>/<boardName>`. 

You will also require a trello api key and api token. In order to generate these, ensure you are logged in to trello and then navigate to https://trello.com/app-key. At the top of the page will be your api key, and then below that a link to manually generate a Token. Clicking on this link will open a screen request you to confirm you are granting access to your boards, when you confirm this you will be presented with an api token. You should save the api key and token in your .env file, as the values of the TRELLO_API_KEY and TRELLO_API_SECRET variables respectively.

More information about generation api keys and tokens for trello can be found [here](https://developer.atlassian.com/cloud/trello/guides/rest-api/api-introduction/)


## Running the app using docker

There is a multi-stage docker file for this project, containing a production build and a development build:

### Production:
- To produce the image: `docker build --target production --tag todo-app:prod .`
- To run: `docker run -p 5100:80 -d --env-file .env todo-app:prod`

The app will then run be accessible on localhost:5100.

### Development: 

The development container can be launched using `docker-compose up -d`. The app can then be accessed at localhost:5000 and will reload whenever changes are made to the app files locally.

 If you would prefer to build and run the image and container manually:
- To produce the image: `docker build --target development --tag todo-app:dev .`
- To run `docker run -p 5000:5000 -d --env-file .env --mount type=bind,source="$(pwd)",target=/app todo-app:dev`
  



## Virtual environment setup

The project uses a virtual environment to isolate package dependencies. The project uses poetry, and the virtual environment can be set up either locally or using Vagrant to run it on a virtual machine.


### Running the project using vagrant

In order to run the project using vagrant you must have installed a Hypervisor , VirtualBox is recommended. You must also download and install vagrant from the [official website](https://www.vagrantup.com/). 


 To create the virtual environment and install required packages, run the following from a bash shell terminal, in the project root directory:

```bash
$ vagrant up
```

Running the `vagrant up` command will cause the app to run as a background process, visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

To stop the app running, destroy the virtual machine using

```bash
$ vagrant destroy
```

##### Running the tests

To run the tests when using Vagrant you must access the vagrant shell using 
```bash
$ vagrant ssh
```

To run the tests navigate to the project directory by running
```bash
$ cd /vagrant
```
and then run the tests using
```bash
$ poetry run pytest
```

### Running the project locally using poetry

To run the project locally you must have poetry installed, installation instructions can be found at https://pypi.org/project/poetry/.

To create the virtual environment and install required packages, run the following from a bash shell terminal, in the project root directory:

```bash
poetry install
```

#### Running the app
Once the poetry install is complete, and the .env file set up, start the Flask app by running:
```bash
$ poetry run flask run
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


#### Running the tests

In order to run the tests you need to install the Firefox browser, and GeckoDriver. the geckodriver executable needs to be placed either in the project root directory, or in a location which is on your path.

Tests can be run from the command line by running: 

```bash
$ poetry run pytest
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

