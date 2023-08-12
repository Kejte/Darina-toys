#! /bin/sh

set -o errexit
set -o nounset

python manage.py collectstatic --no-input
python manage.py makemigrations --no-input && python manage.py migrate
python manage.py migrate
gunicorn --bind 0.0.0.0:8000 --timeout 240 darinatoys.wsgi:application --log-level debug -w 4 --reload
