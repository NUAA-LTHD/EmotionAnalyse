from django.urls import path,include
from api import views as api_views
from login import views as login_views
from . import views
from . import HTTP_ERROR
from django.contrib import admin
urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'',views.index),
    path(r'login/',login_views.login),
    path(r'register/',login_views.register),
    path(r'logout/',login_views.logout),
    path(r'email/',api_views.email),
    path(r'api/',api_views.api),
    path(r'token/',api_views.token),
    path(r'index/',include("index.urls")),
]
handler404 = HTTP_ERROR.not_found