"""
Production Settings for Heroku
"""

import environ
import django_heroku

# If using in your own project, update the project namespace below
from bundle.settings.base import *

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, True)
)

# False if not in os.environ
DEBUG = env('DEBUG')

# Raises django's ImproperlyConfigured exception if SECRET_KEY not in os.environ
SECRET_KEY = env('SECRET_KEY')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

# Parse database connection url strings like psql://user:pass@127.0.0.1:8458/db



# Django-Heroku Setup
django_heroku.settings(locals())