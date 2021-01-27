#!/usr/bin/env sh

set -eou pipefail;

COMMAND="$*";

while ! nc -z "${DB_HOST}" "${DB_PORT}";
do
  echo 'Waiting for postgres...';
  sleep 5;
done;

cd /opt/sati;
python manage.py migrate;
python manage.py collectstatic --no-input -v0;

# shellcheck disable=SC2086
exec $COMMAND;
