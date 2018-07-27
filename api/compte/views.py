from rest_framework import generics, status
from rest_framework.response import Response
from django_filters import rest_framework as filters
from rest_framework.permissions import *
from api.models import *
from . import serializers


class ComptesList(generics.ListCreateAPIView):
    queryset = Compte.objects.all()
    serializer_class = serializers.CompteBasicSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('num_compte', 'id', 'solde', 'date_ouverture', 'date_fermeture')
    permission_classes = (IsAdminUser,)

    # compte/
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ComptesId(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.CompteBasicSerializer
    permission_classes = (IsAdminUser,)

    # compte/:id
    def get_queryset(self):
        return Compte.objects.filter()

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    """Il faut rajouter la condition de refuser les methodes"""


class ComptesIdTransaction(generics.ListAPIView):
    serializer_class = serializers.CompteTransactionSerializer
    permission_classes = (IsAdminUser,)

    # compte/:id/transaction
    def get_queryset(self):
        return Compte.objects.filter(pk=self.kwargs['pk'])
