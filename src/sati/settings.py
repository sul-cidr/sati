""" SATI :: Django Settings """

import os

import dj_database_url
from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

from .baton_settings import BATON  # noqa: F401

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = os.environ.get("DEBUG", "true").lower() == "true"

if not DEBUG and "SECRET_KEY" not in os.environ:
    # a new SECRET_KEY can be generated with
    #  python -c "import secrets; print(secrets.token_urlsafe())"
    raise ImproperlyConfigured("Don't use the default SECRET_KEY in production!")

SECRET_KEY = os.environ.get(
    "SECRET_KEY", "jl%^r)&^hl6ttj$%(q4tx1ym7z5)eq^zg&7cmx6(yns%l77g%b"
)


ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1,0.0.0.0").split(",")
INTERNAL_IPS = ("127.0.0.1",)

# Application definition
INSTALLED_APPS = [
    "baton",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.forms",
    "pagedown.apps.PagedownConfig",
    "sati.users",
    "sati.items",
    "baton.autodiscover",
]

if DEBUG:
    INSTALLED_APPS += ["django_extensions", "debug_toolbar"]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "sati.middleware.TimezoneMiddleware",
]

if DEBUG:
    MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE


ROOT_URLCONF = "sati.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "sati", "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

WSGI_APPLICATION = "sati.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
if "DATABASE_URL" not in os.environ:
    os.environ[
        "DATABASE_URL"
    ] = "postgres://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}".format(
        **os.environ
    )

DATABASES = {"default": dj_database_url.config(conn_max_age=600)}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

AUTH_USER_MODEL = "users.User"


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = False
USE_L10N = False
USE_TZ = True

MEDIA_ROOT = os.getenv("MEDIA_ROOT", os.path.join(BASE_DIR, "media"))
MEDIA_URL = os.getenv("MEDIA_URL", "/media/")

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_ROOT = os.getenv("STATIC_ROOT", os.path.join(BASE_DIR, "static"))
STATIC_URL = os.getenv("STATIC_URL", "/static/")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "assets")]
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

ADMINS = (
    [tuple(_.split(",")) for _ in os.getenv("ADMINS", None).split(";")]
    if os.getenv("ADMINS", None)
    else []
)
