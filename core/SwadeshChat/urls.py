from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('chat/<str:slug>', chatbox, name="chat"),
    path('chat/<str:slug>/refresh', get_chatdata, name="get_chatdata"),
    path('add_contact/<int:user_id>', add_contact, name="add_contact"),
    path('create_group/', create_group, name="create_group")
]