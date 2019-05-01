#!/bin/bash

# # Apply database migrations
# echo "Make database migrations"
# python manage.py makemigrations

# # Apply database migrations
# echo "Apply database migrations"
# python manage.py migrate

# # Apply database migrations
# echo "Collect statics"
# python manage.py collectstatic --noinput

echo "Running command '$*'"
exec $*