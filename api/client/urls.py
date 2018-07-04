from django.conf.urls import url
from django.urls import include, path
from . import views

urlpatterns = [
    path('client', views.ClientList.as_view()),
    path('client/<int:pk>', views.ClientId.as_view()),
    path('client/<int:pk>/adresse', views.ClientIdAdresses.as_view()),
    path('client/<int:pk>/compte', views.ClientIdCompte.as_view()),
    path('client/<int:pk>/compte/<int:pk_compte>', views.ClientIdCompteId.as_view()),
    path('client/search?param=x', views.ClientSearch.as_view()),
]