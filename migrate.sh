#!bin/bash

# Use the ENV Variable or use a default
DJANGO_SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-'admin@example.com'}
DJANGO_SUPERUSER_PASSWORD=${DJANGO_SUPERUSER_PASSWORD:-'testing321'}

python manage.py migrate --noinput
python manage.py createsuperuser --email $DJANGO_SUPERUSER_EMAIL --noinput || true


python manage.py createsuperuser --email admin@example.com
