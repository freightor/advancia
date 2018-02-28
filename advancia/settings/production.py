from .base import *
import os
import dj_database_url

DEBUG = os.environ.get("DB_DEBUG")
ALLOWED_HOSTS = [".herokuapp.com"]
SECRET_KEY = os.environ.get('SECRET_KEY')
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
DATABASES = {
    'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))
}
