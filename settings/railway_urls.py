"""
URL config for Railway: the regular wger URLs plus uploaded media files,
which would otherwise be served by nginx.
"""

# Django
from django.conf import settings
from django.urls import re_path
from django.views.static import serve

# wger
from wger.urls import urlpatterns as wger_urlpatterns

urlpatterns = [
    re_path(
        rf'^{settings.MEDIA_URL.strip("/")}/(?P<path>.*)$',
        serve,
        {'document_root': settings.MEDIA_ROOT},
    ),
    *wger_urlpatterns,
]
