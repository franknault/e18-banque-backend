from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from . import serializers
from api.models import *
from django_filters import rest_framework as filters


class ClientList(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = serializers.ClientSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    permission_classes = (IsAdminUser,)

    #@IsAdminUser
    def get_queryset(self):
        return Client.objects.all()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ClientId(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = serializers.ClientSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    permission_classes = (IsAdminUser, IsAuthenticated)

    def get_queryset(self):
        return Client.objects.filter(pk=self.kwargs['pk'])

    #@IsAdminUser
    def put(self, request, *args, **kwargs):
        return self.put(request, *args, **kwargs)

    #@IsAdminUser
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ClientIdAdresses(generics.RetrieveUpdateDestroyAPIView, generics.CreateAPIView):
    queryset = Adresse.objects.all()
    serializer_class = serializers.ClientsAdresseSerializer
    filter_backends = (filters.DjangoFilterBackend, )
    permission_classes = (IsAdminUser, IsAuthenticated, )

    #@IsAuthenticated
    def get_queryset(self):
        return Adresse.objects.filter(pk=self.kwargs['pk'])

    #@IsAdminUser
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    #@IsAdminUser
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class ClientIdCompte(generics.RetrieveAPIView):
    serializer_class = serializers.ClientsAdresseSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return Courant.objects.filter(id=self.kwargs['id'])


class ClientIdCompteId(generics.RetrieveAPIView):
    serializer_class = serializers.ClientsAdresseSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        query_courant = Courant.objects.filter()
        return query_courant.filter(pk=self.kwargs['pk_compte'])


class ClientSearch(generics.RetrieveAPIView):
    serializer_class = serializers.ClientSerializer
    filter_backends = (filters.DjangoFilterBackend, )
    permission_classes = (IsAdminUser, )
    #filter_fields = ('telephone', 'type', 'nom_particulier', 'prenom_particulier', 'nom_entreprise', 'numero_entreprise',)

    def get_queryset(self):
        return Client.objects.filter()