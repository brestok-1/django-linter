from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter

from django.core.asgi import get_asgi_application

import checker.routing

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_linter.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    "websocket": URLRouter(checker.routing.websocket_urlpatterns),
})
