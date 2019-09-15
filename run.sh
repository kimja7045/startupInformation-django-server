#!/bin/bash
source /home/ubuntu/.venv/bin/activate

python manage.py migrate
python manage.py collectstatic
exec uwsgi --ini env/uwsgi.ini
