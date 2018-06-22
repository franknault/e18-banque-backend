from django.conf.urls import url
from django.urls import include, path
from . import views

urlpatterns = [
    path('client', views.ClientsList.as_view()),
    path('client/<int:pk>', views.ClientsList.as_view()),
    path('client/<int:pk>/adresse', views.ClientsList.as_view()),
    path('client/<int:pk>/compte', views.ClientsIdCompte.as_view()),
    path('client/<int:pk>/compte/<int:pk>', views.ClientsIdCompteId.as_view()),
]