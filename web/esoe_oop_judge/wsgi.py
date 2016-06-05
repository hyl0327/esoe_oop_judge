"""
WSGI config for esoe_oop_judge project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application


os.environ['DJANGO_SETTINGS_MODULE'] = 'esoe_oop_judge.settings'

application = get_wsgi_application()
