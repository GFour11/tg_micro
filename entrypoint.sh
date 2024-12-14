#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python userservice/manage.py collectstatic --noinput
python userservice/manage.py makemigrations
python userservice/manage.py migrate

exec "$@"
