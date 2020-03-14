from django.urls import path,include,re_path
from api import views as api_views
from login import views as login_views
from django.views import static
from .settings import MEDIA_ROOT,STATIC_ROOT
from . import views
from . import HTTP_ERROR

import xadmin
urlpatterns = [
    path(r'xadmin/', xadmin.site.urls),
    path(r'',views.index),
    path(r'login/',login_views.login),
    path(r'register/',login_views.register),
    path(r'logout/',login_views.logout),
    path(r'email/',api_views.email),
    path(r'api/',api_views.api),
    path(r'token/',api_views.token),
    path(r'index/',include("index.urls")),
    path(r'ueditor/',include('DjangoUeditor.urls')),
    re_path('^static/(?P<path>.*)$', static.serve, {'document_root': STATIC_ROOT}, name='static'),
    re_path(r'^media/(?P<path>.*)$',static.serve,{"document_root":MEDIA_ROOT},name='media'),
]
handler404 = HTTP_ERROR.not_found