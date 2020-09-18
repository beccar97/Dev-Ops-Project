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