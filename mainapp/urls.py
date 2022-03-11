from django.urls import path
from django.urls.conf import include
from .views import *

urlpatterns = [
    path('',listofmovies.as_view(),name="main"),
    path('comments/selectlang/<int:id>/',selectlang.as_view(),name="selectlang"),
    path('comments/<int:id>/<str:lang>/',listofcomments.as_view(),name="comments"),
    path('uploadcomment/<int:id>/',uploadvoicecomment.as_view(),name='uploadcomment'),
]
