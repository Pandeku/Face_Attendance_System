# -*- coding:UTF-8 -*-
"""
WSGI config for Face_Attendance_System project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Face_Attendance_System.settings")

application = get_wsgi_application()
