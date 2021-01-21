#!/usr/bin/env sh

set -eou pipefail;

cmd="$*";

cd /opt/sati;
python manage.py migrate;
python manage.py collectstatic --no-input -v0;


exec $cmd
