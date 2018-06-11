from django.conf.urls import url
from django.urls import path
from api.administrateur.views import *
from . import views

urlpatterns = [
    path('compte', views.ComptesList.as_view()),
    path('compte/<int:pk>', views.ComptesId.as_view()),
    path('compte/<num_compte>', views.ComptesId.as_view()),
    path('compte/<int:pk>/transaction', views.ComptesIdTransaction.as_view())
]