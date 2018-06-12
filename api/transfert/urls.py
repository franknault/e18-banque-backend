from django.conf.urls import url
from django.urls import path

from . import views


urlpatterns = [
    path('transfert', views.TransfertFreeze.as_view())
]