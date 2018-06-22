from django.conf.urls import url
from django.urls import include, path
from . import views

urlpatterns = [
    url(r'^clients/entreprises$', views.ClientsEntrepriseApi.as_view()),
    url(r'^clients/particuliers$', views.ClientsParticulierApi.as_view()),
    url(r'^clients$', views.ClientsList.as_view()),
    path('rest-auth/', include('rest_auth.urls')),

    path('client', views.ClientsList.as_view()),
    path('client/<int:pk>', views.ClientsList.as_view()),
    path('client/<int:pk>/adresse', views.ClientsList.as_view()),

]