from django.urls import path,include
from api import views as api_views
from . import HTTP_ERROR
from django.contrib import admin
urlpatterns = [
    path(r'api/',api_views.api),
    path(r'token/',api_views.token),
    path(r'index/',include("index.urls")),
]
handler404 = HTTP_ERROR.not_found