#!/bin/bash

if [[ -n $(psql -d "${DB_NAME}" -c '\q' 2>&1) ]];
then
  createdb "${DB_NAME}";
  createuser --superuser "${DB_USER}";
  psql -c "ALTER USER ${DB_USER} WITH password '${DB_PASSWORD}';";
fi;
