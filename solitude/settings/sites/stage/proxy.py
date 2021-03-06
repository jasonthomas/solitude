"""private_base will be populated from puppet and placed in this directory"""

import logging

import private_base as private

from solitude.settings import base
from django_sha2 import get_password_hashers


ADMINS = ()
ALLOWED_HOSTS = ['*']

DATABASES = {'default': {}}

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

SYSLOG_TAG = 'http_app_payments_stage'
TEMPLATE_DEBUG = DEBUG

# Solitude specific settings.
AES_KEYS = {}

CLEANSED_SETTINGS_ACCESS = True
CLIENT_JWT_KEYS = private.CLIENT_JWT_KEYS

NEWRELIC_INI = '/etc/newrelic.d/payments-proxy.allizom.org.ini'
NOSE_PLUGINS = []

REQUIRE_OAUTH = False

# Below is configuration of payment providers.

PAYPAL_APP_ID = private.PAYPAL_APP_ID
PAYPAL_AUTH = private.PAYPAL_AUTH
PAYPAL_CHAINS = private.PAYPAL_CHAINS
PAYPAL_URLS_ALLOWED = ('https://marketplace.allizom.org',)
PAYPAL_USE_SANDBOX = True

BANGO_ENV = 'prod'
BANGO_AUTH = private.BANGO_AUTH

ZIPPY_CONFIGURATION = {
    'boku': {
        'url': base.BOKU_API_DOMAIN,
    }
}

BOKU_MERCHANT_ID = private.BOKU_MERCHANT_ID
BOKU_SECRET_KEY = private.BOKU_SECRET_KEY
