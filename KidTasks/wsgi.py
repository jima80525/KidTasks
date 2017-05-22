"""
WSGI config for KidTasks project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "KidTasks.settings")

application = get_wsgi_application()  # pylint: disable=invalid-name
application = DjangoWhiteNoise(application)  # pylint: disable=invalid-name
