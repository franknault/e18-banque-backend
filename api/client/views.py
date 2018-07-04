from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from . import serializers
from api.models import *
from django_filters import rest_framework as filters


class ClientList(generics.ListCreateAPIView):
    """API pour créer un client et obtenir la liste des clients"""

    queryset = Client.objects.all()
    serializer_class = serializers.ClientSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    permission_classes = (IsAdminUser,)

    """
    GET Methode > CHEK
    Route : client    
    """
    #@IsAdminUser
    def get_queryset(self):
        return Client.objects.all()

    """
    POST Methode
    Route : client
    """
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ClientId(generics.RetrieveUpdateDestroyAPIView):
    """API de gestion d'un client """
    queryset = Client.objects.all()
    serializer_class = serializers.ClientSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    permission_classes = (IsAdminUser, IsAuthenticated)

    """
    GET Methode > CHEK
    Route : client/:idClient
    """
    def get_queryset(self):
        return Client.objects.filter(pk=self.kwargs['pk'])

    """
    PUT Methode > CHEK
    Route : client/:idClient
    """
    #@IsAdminUser
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    """
    DELETE Methode
    Route : client/:idClient
    """
    #@IsAdminUser
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ClientIdAdresses(generics.RetrieveUpdateDestroyAPIView, generics.CreateAPIView):
    """API de gestion d'adresses pour un client"""
    serializer_class = serializers.ClientsAdresseSerializer
    filter_backends = (filters.DjangoFilterBackend, )
    permission_classes = (IsAdminUser, IsAuthenticated, )

    """
    GET Methode > CHECK
    Route : client/:idClient/adresse
    """
    #@IsAuthenticated
    def get_queryset(self):
        return Client.objects.filter(pk=self.kwargs['pk'])

    """
    PATCH Methode > CHECK
    Route : client/:idClient/adresse
    """
    #@IsAdminUser
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    """
    DELETE Methode > CHECK
    Route : client/:idClient/adresse
    """
    #@IsAdminUser
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    """
    POST Methode 
    Route : client/:idClient/adresse
    """
    def post(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class ClientIdCompte(generics.RetrieveAPIView):
    """"API de gestion de compte pour un client"""
    serializer_class = serializers.ClientCompteSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    permission_classes = (IsAuthenticated, )

    """
    GET Methode
    Route : client/:idClient/compte
    """
    def get_queryset(self):
        return Client.objects.filter(pk=self.kwargs['pk'])


class ClientIdCompteId(generics.RetrieveAPIView):
    """API de gestion d'un id de compte par rapport a un client"""
    serializer_class = serializers.ClientCompteSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    permission_classes = (IsAuthenticated, )

    """
    GET Methode
    Route : client/:idClient/compte/:idCompte
    """
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