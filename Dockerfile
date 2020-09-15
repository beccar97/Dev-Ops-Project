FROM python:3.8.5-slim-buster

RUN pip install poetry
WORKDIR /app
COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install --no-root

COPY . .
RUN poetry install

EXPOSE 5000
ENTRYPOINT [ "poetry", "run", "gunicorn", "-b 0.0.0.0:5000", "src.app:create_app()"]