FROM python:3.8.5-slim-buster as base

RUN pip install poetry
WORKDIR /app
COPY pyproject.toml .
COPY poetry.lock .

FROM base as production
RUN poetry install --no-root --no-dev
COPY ./src ./src
EXPOSE 80
ENTRYPOINT [ "poetry", "run", "gunicorn", "-b 0.0.0.0:80", "src.app:create_app()"]

FROM base as development
RUN poetry install --no-root
EXPOSE 5000
ENTRYPOINT ["poetry", "run", "flask", "run", "--host=0.0.0.0"]

FROM development as test
# Install curl
WORKDIR /usr/local/bin
RUN apt-get update &&\
    apt-get install curl -y -q
# Install Chrome
RUN curl -sSL https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o chrome.deb &&\ 
    apt-get install ./chrome.deb -y &&\
    rm ./chrome.deb  
# Install Chromium WebDriver 
RUN LATEST=`curl -sSL https://chromedriver.storage.googleapis.com/LATEST_RELEASE` &&\
    echo "Installing chromium webdriver version ${LATEST}" &&\
    curl -sSL https://chromedriver.storage.googleapis.com/${LATEST}/chromedriver_linux64.zip -o chromedriver_linux64.zip &&\
    apt-get install unzip -y &&\
    unzip ./chromedriver_linux64.zip
WORKDIR /app
ENTRYPOINT [ "poetry", "run", "pytest" ]
