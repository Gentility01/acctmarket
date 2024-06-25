#!/bin/sh

# Your series of commands
exec python manage.py migrate
# exec /usr/local/bin/gunicorn config.asgi --bind 0.0.0.0:5000 --chdir=/app -k uvicorn.workers.UvicornWorker
exec python manage.py runserver 0.0.0.0:5000
