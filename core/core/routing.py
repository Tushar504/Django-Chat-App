from django.urls import path , include
from .consumers import ChatConsumer
 

websocket_urlpatterns = [
    path("<group_slug>" , ChatConsumer.as_asgi()) , 
]