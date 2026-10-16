# ruff: noqa: F405
"""
Settings for running wger on Railway.

Railway has no nginx sidecar, so static files are served by WhiteNoise and
uploaded media by Django itself (see settings/railway_urls.py).
"""

# wger
from .main import *  # noqa: F403

MIDDLEWARE.insert(
    MIDDLEWARE.index('django.middleware.common.CommonMiddleware'),
    'whitenoise.middleware.WhiteNoiseMiddleware',
)

ROOT_URLCONF = 'settings.railway_urls'

# Railway terminates TLS and forwards the original host/scheme
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
