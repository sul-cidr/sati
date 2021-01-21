#!/usr/bin/env sh

set -eou pipefail;

cmd="$*";

while ! nc -z "${DB_HOST}" "${DB_PORT}";
do
  echo 'Waiting for postgres...';
  sleep 5;
done;

cd /opt/sati;
python manage.py migrate;
python manage.py collectstatic --no-input -v0;

exec $cmd;
