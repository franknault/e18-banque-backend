from django.conf.urls import url
from django.urls import path
from api.administrateur.views import *
from . import views

urlpatterns = [
    path('compte', views.Comptes.as_view()),
    path('compte/<int:pk>', views.ComptesId.as_view()),
    path('compte/<int:pk>/transaction', views.ComptesIdTransaction.as_view())
]