#!/bin/sh
poetry run gunicorn -b 0.0.0.0:$PORT 'src.app:create_app()'