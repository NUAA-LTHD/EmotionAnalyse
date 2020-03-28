from django.urls import path
from index import views
urlpatterns=[
    path(r'',views.index),
    path(r'doc/<title>/',views.doc),
    path(r'write/',views.write),
    path(r'view/',views.view),
    path(r'mine/',views.mine),
    path(r'articles',views.articles),
    path(r'articles/<page>',views.articles)
]