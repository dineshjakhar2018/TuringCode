"""
WSGI config for TuringCode project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from dj_static import Cling,MediaCling
from static_ranges import Ranges


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TuringCode.settings')

#default 
#application = get_wsgi_application()

#application = MediaCling(get_wsgi_application())

application = Ranges(Cling(MediaCling(get_wsgi_application())))
