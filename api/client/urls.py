from django.conf.urls import url
from api.client.views import *
from django.urls import include, path

urlpatterns = [
    url(r'^clients/entreprises$', ClientsEntrepriseApi.as_view()),
    url(r'^clients/particuliers$', ClientsParticulierApi.as_view()),
    url(r'^clients$', ClientsApi.as_view()),
    path('rest-auth/', include('rest_auth.urls'))
]