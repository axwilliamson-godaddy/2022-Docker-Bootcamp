#!/bin/bash

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python manage.py makemigrations polls
python manage.py migrate

echo "Setup superuser"
export DJANGO_SUPERUSER_PASSWORD=bootcamp
python manage.py createsuperuser --noinput --username admin --email test@test.com || echo "User already exists"

# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8000