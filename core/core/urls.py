from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include("SwadeshChat.urls")),
    path('admin/', admin.site.urls),
    path("api/auth/", include("user_auth.urls"))

]
