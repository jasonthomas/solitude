"""private_base will be populated from puppet and placed in this directory"""

import logging

import dj_database_url

import private_base as private

from solitude.settings import base
from django_sha2 import get_password_hashers


ADMINS = ()
ALLOWED_HOSTS = ['payments-dev.allizom.org', 'localhost']

DATABASES = {}
DATABASES['default'] = dj_database_url.parse(private.DATABASES_DEFAULT_URL)
DATABASES['default']['ENGINE'] = 'django.db.backends.mysql'
DATABASES['default']['OPTIONS'] = {'init_command': 'SET storage_engine=InnoDB'}

DEBUG = False
DEBUG_PROPAGATE_EXCEPTIONS = False

HMAC_KEYS = private.HMAC_KEYS

PASSWORD_HASHERS = get_password_hashers(base.BASE_PASSWORD_HASHERS, HMAC_KEYS)

LOG_LEVEL = logging.DEBUG

SECRET_KEY = private.SECRET_KEY

SENTRY_DSN = private.SENTRY_DSN

STATSD_HOST = private.STATSD_HOST
STATSD_PORT = private.STATSD_PORT
STATSD_PREFIX = private.STATSD_PREFIX

SYSLOG_TAG = 'http_app_payments_dev'
TEMPLATE_DEBUG = DEBUG

# Solitude specific settings.
AES_KEYS = private.AES_KEYS

CLEANSED_SETTINGS_ACCESS = True
CLIENT_OAUTH_KEYS = private.CLIENT_OAUTH_KEYS

SITE_URL = 'https://payments-dev.allizom.org'

S3_AUTH = {'key': private.S3_AUTH_KEY, 'secret': private.S3_AUTH_SECRET}
S3_BUCKET = private.S3_BUCKET

NEWRELIC_INI = '/etc/newrelic.d/payments-dev.allizom.org.ini'

# Below is configuration of payment providers.

ZIPPY_PROXY = 'https://payments-proxy-dev.allizom.org/proxy/provider'
ZIPPY_CONFIGURATION = {
    'reference': {
        'url': 'https://zippy-dev.allizom.org'
    },
    'boku': {
        'url': base.BOKU_API_DOMAIN
    }
}

PAYPAL_PROXY = private.PAYPAL_PROXY
PAYPAL_URLS_ALLOWED = ('https://marketplace-dev.allizom.org',)

BANGO_BASIC_AUTH = private.BANGO_BASIC_AUTH
BANGO_FAKE_REFUNDS = True
BANGO_PROXY = private.BANGO_PROXY
BANGO_NOTIFICATION_URL = (
    'https://marketplace-dev.allizom.org/mozpay/bango/notification')


BOKU_PROXY = ZIPPY_PROXY

NOSE_PLUGINS = []
