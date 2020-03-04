from django.urls import path,include
from api import views as api_views
from index import views as index_views
from . import views
from . import HTTP_ERROR
from django.contrib import admin
admin.autodiscover()
urlpatterns = [
    path(r'',views.index),
    path(r'api/',api_views.api),
    path(r'token/',api_views.token),
    path(r'index/',include("index.urls")),
]
handler404 = HTTP_ERROR.not_found