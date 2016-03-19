"""
WSGI config for system project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import sys
 
sys.path.append("/usr/ticsup/ticsystem/lib/python2.7/site-packages")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "system.settings")
 
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()