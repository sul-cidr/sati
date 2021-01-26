[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Test](https://github.com/sul-cidr/sati/workflows/Test/badge.svg)](https://github.com/sul-cidr/sati/actions?query=workflow%3ATest)

# Semiotic Analysis of Test Items

## Development

With a working version of Python 3.8 and Pipenv:

1. Install dependencies (use `sync` instead of `install` to use `Pipfile.lock` instead, and ensure a deterministic environment).

   ```
   $ pipenv sync --dev
   ```

2. Install pre-commit hooks.

   ```
   $ pipenv run pre-commit install
   ```

3. Create a database (if not created yet) and migrate. Only PostgreSQL is supported. Database settings must be specified in a `.env` file (see [`.env_tempate`](.env_template) for details).

   ```
   $ pipenv run python manage.py migrate
   ```

4. Create a superuser.

   ```
   $ pipenv run python manage.py createsuperuser
   ```

5. Collect static files from installed apps.

   ```
   $ pipenv run python manage.py collectstatic
   ```

6. Start development server and go to `http://localhost:8000/admin/`.

   ```
   $ pipenv run python manage.py runserver localhost:8000
   ```

## Testing

- Tests

  ```
  $ pipenv run python manage.py test
  ```

- Linting and formatting
  ```
  $ pipenv run pre-commit run --all-files
  ```

## Production

A production-ready deployment can be brought up with just `docker-compose up --build [-d]`. This will start a container for the django app and another for the PostgreSQL database server. Note that the app is via `gunicorn` on port 8000 which is exposed to the docker host, and the `/static` and `/media` roots are mounted from the host filesystem, as this is intended to be run behind a webserver on the docker host which serves up `/static` and `/media` and reverse-proxies the app.

Running the Django development server is possible with a command like the example below, but note that the docker image is compiled without installing the Django dev. dependencies.

```
docker-compose run --rm --name sati-app -p 8000:8000 django python manage.py runserver 0.0.0.0:8000
```

See the notes in [`.env_tempate`](.env_template) for further details.
