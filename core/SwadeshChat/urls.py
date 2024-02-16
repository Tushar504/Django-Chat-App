from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('chat/<str:slug>', chatbox, name="chat"),
    path('add_contact/<int:user_id>', add_contact, name="add_contact"),
    path('create_group/', create_group, name="create_group")
]