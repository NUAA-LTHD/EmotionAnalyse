from django.urls import path
from index import views
urlpatterns=[
    path(r'doc/<title>/',views.doc)
]