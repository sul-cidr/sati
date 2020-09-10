[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![Test](https://github.com/sul-cidr/sati/workflows/Test/badge.svg)

# Semiotic Analysis of Test Items


## Development
With a working version of Python 3.8 and Pipenv:

1. Install dependencies (use `sync` instead of `install` to use `Pipfile.lock` instead, and ensure a deterministic enviroment).
	```
	$ pipenv sync --dev
	```

2. Install pre-commit hooks.
	```
	$ pipenv run pre-commit install
	```

3. Create a database (if not created yet) and migrate.  Only PostgreSQL is supported.  A `DATABASE_URL` can be defined in a `.env` file or set as an environment variable. See [`.env_tempate`](.env_template) and [here](https://github.com/kennethreitz/dj-database-url#url-schema) for details.
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
