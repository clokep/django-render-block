SECRET_KEY = 'not_empty'
SITE_ID = 1

DATABASE_ENGINE = 'sqlite3',

MIDDLEWARE_CLASSES = tuple()

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

INSTALLED_APPS = (
    'tests',
)
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)
