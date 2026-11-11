#!/bin/sh
set -e

python manage.py migrate --no-input
python manage.py loaddata method_categories
python manage.py collectstatic --no-input --clear

exec "$@"
