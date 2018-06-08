from rest_framework.generics import ListAPIView

from .serializers import *
from api.models import Client


class ClientsApi(ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ClientsEntrepriseApi(ListAPIView):
    queryset = Client.objects.filter(type=Client.ENTREPRISE).all()
    serializer_class = ClientEntreprise


class ClientsParticulierApi(ListAPIView):
    queryset = Client.objects.filter(type=Client.PARTICULIER).all()
    serializer_class = ClientParticulier

