from django.conf.urls import url
from api.client.api import *

urlpatterns = [
    url(r'^clients/entreprises$', ClientsEntrepriseApi.as_view()),
    url(r'^clients/particuliers$', ClientsParticulierApi.as_view()),
    url(r'^clients$', ClientsApi.as_view()),
    url(r'^clients$', ClientsApi.as_view())
]