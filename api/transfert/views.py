from rest_framework import generics, status
from django_filters import rest_framework as filters
from api.models import *
from . import serializers


class Transfert(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = serializers.TransfertBasicSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('etat', 'id', 'montant', 'type_transaction', 'date_debut', 'date_fin')


    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)