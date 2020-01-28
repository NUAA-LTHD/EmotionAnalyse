from django.urls import path
from . import HELLO
from . import API
from . import INDEX
from . import HTTP_ERROR
urlpatterns = [
    path('hello/',HELLO.hello),
    path('api/',API.api),
    path('token/',API.token),
    path('doc/<title>',INDEX.doc)
]
#handler404 = HTTP_ERROR.not_found