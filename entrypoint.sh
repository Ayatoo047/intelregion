#!/bin/sh


python manage.py makemigrations
python manage.py migrate
pytest

# Start the Django server
exec "$@"