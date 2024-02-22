from django.urls import path
from .consumers import ChatConsumer


websocket_urlpatterns = [
    path("<group_slug>", ChatConsumer.as_asgi())
]
