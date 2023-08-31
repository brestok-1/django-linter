from django.urls import path

from checker.consumers import FileCheckConsumer, EmailSendComsumer

websocket_urlpatterns = [
    path('ws/file_check/', FileCheckConsumer.as_asgi()),
    path('ws/email_send/', EmailSendComsumer.as_asgi()),
]
