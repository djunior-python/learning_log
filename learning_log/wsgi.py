"""
WSGI config for learning_log project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'learning_log.settings')

application = get_wsgi_application()


User = get_user_model()
if not User.objects.filter(user_name="admin").exists():
    User.objects.create_superuser(
        user_name="admin",
        email="admin@example.com",
        password=os.environ.get("DJANGO_SUPERUSER_PASSWORD", "holypython123")
    )
