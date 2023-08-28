from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter

from django.core.asgi import get_asgi_application
from django.urls import path

from checker.consumers import FileCheckConsumer

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_linter.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path('ws/file_check', FileCheckConsumer.as_asgi())
        ])
    )
})
