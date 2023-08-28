from django.urls import path

from checker.consumers import FileCheckConsumer

websocket_urlpatterns = [
    path(r'ws/file_check/', FileCheckConsumer.as_asgi()),
]