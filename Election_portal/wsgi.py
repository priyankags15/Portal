"""
WSGI config for Election_portal project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

#Wrong!
#sys.path.append("/home/user/mysite/mysite")

#Correct
#sys.path.append("/home/user/mysite")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Election_portal.settings")

application = get_wsgi_application()
