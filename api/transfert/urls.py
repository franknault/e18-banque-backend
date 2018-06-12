from django.urls import path
from . import views


urlpatterns = [
    path('transfert', views.Transfert.as_view())
]