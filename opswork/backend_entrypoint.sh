#!/bin/bash
service cron start
cd /django/
/opt/venv/bin/python manage.py migrate

# Use the ENV Variable or use a default
# STEVE=${STEVE:-'developer@stephenkinyua.co.ke'}
# KAWSER=${KAWSER:-'kawser.ahmed.dev@gmail.com'}
# ANORLD=${ANORLD:-'anorldlifereze63@gmail.com'}
# DJANGO_SUPERUSER_PASSWORD=${DJANGO_SUPERUSER_PASSWORD:-'veetaworkplace!@#'}

# /opt/venv/bin/python manage.py createsuperuser --email $STEVE --first_name Stevie --last_name Dev --noinput || true
# /opt/venv/bin/python manage.py createsuperuser --email $KAWSER --first_name Anorld --last_name Lifereze --noinput || true
# /opt/venv/bin/python manage.py createsuperuser --email $ANORLD --first_name Kawser --last_name Ahmed --noinput || true

/opt/venv/bin/gunicorn --worker-tmp-dir /dev/shm core.wsgi:application --bind "0.0.0.0:8000"
