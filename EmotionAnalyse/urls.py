from django.urls import path
from . import HELLO
from . import API
urlpatterns = [
    path('hello/',HELLO.hello),
    path('api/',API.api),
    path('token/',API.token)
]