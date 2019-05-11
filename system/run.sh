#!/bin/sh

>&2 echo "Running migrations"
python /srv/manage.py migrate

>&2 echo "Starting supervisor"
supervisord -c /srv/system/supervisord.conf
