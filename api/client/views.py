from rest_framework.generics import ListAPIView
from .serializers import *
from api.models import *
from rest_framework.generics import CreateAPIView
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import *
from . import serializers
from api.models import *
from django_filters import rest_framework as filters


class ClientId(generics.RetrieveUpdateDestroyAPIView):
    """API de gestion d'un client """
    queryset = Client.objects.all()
    serializer_class = serializers.ClientSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    permission_classes = (IsAdminUser, )

    """
    GET Methode > CHEK
    Route : admin/client/:idClient
    """
    def get_queryset(self):
        return Client.objects.filter(pk=self.kwargs['pk'])

    """
    PUT Methode > CHEK
    Route : admin/client/:idClient
    """
    #@IsAdminUser
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    """
    DELETE Methode
    Route : admin/client/:idClient
    """
    #@IsAdminUser
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ClientIdAdresses(generics.RetrieveUpdateDestroyAPIView, generics.CreateAPIView):
    """API de gestion d'adresses pour un client"""
    serializer_class = serializers.ClientsAdresseSerializer
    filter_backends = (filters.DjangoFilterBackend, )
    permission_classes = (IsAdminUser, )

    """
    GET Methode > CHECK
    Route : admin/client/:idClient/adresse
    """
    def get_queryset(self):
        return Client.objects.filter(pk=self.kwargs['pk'])

    """
    PATCH Methode > CHECK
    Route : admin/client/:idClient/adresse
    """
    def patch(self, request, *args, **kwargs):
        return self.patch(request, *args, **kwargs)

    """
    DELETE Methode > CHECK
    Route : admin/client/:idClient/adresse
    """
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    """
    POST Methode 
    Route : admin/client/:idClient/adresse
    """
    def post(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class ClientIdCompte(generics.RetrieveAPIView):
    """"API de gestion de compte pour un client"""
    serializer_class = serializers.ClientCompteSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    permission_classes = (IsAdminUser, )

    """
    GET Methode > CHECK OK
    Route : admin/client/:idClient/compte
    """
    def get_queryset(self):
        return Client.objects.filter(pk=self.kwargs['pk'])


class ClientIdCompteId(generics.RetrieveAPIView):
    """API de gestion d'un id de compte par rapport a un client"""
    serializer_class = serializers.ClientCompteSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    permission_classes = (IsAdminUser, )

    """
    GET Methode > CHECK OK
    Route : admin/client/:idClient/compte/:idCompte
    """
    def get_queryset(self):
        query_courant = Courant.objects.filter()
        return query_courant.filter(pk=self.kwargs['pk_compte'])


class ClientSearch(generics.RetrieveAPIView):
    serializer_class = serializers.ClientSerializer
    filter_backends = (filters.DjangoFilterBackend, )
    permission_classes = (IsAdminUser, )

    def get_queryset(self):
        return Client.objects.filter()

      
class ClientsApi(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = serializers.ClientSerializerNom
    """
    GET Method
    Route : admin/client/
    """
    def get_queryset(self):
        return Client.objects.all()

    """
    POST Method
    Route : admin/client/
    """
    def post(self, request, *args, **kwargs):

        info = InfoAuthentification.objects.create_user(username=request.data['username'], email=request.data['email'], password=request.data['password'])
        info.save()

        client = Client.objects.create(nom_particulier=request.data['nom_particulier'], prenom_particulier=request.data['prenom_particulier'], sexe=request.data['sexe'],
                              nom_entreprise=request.data['nom_entreprise'], numero_entreprise=request.data['numero_entreprise'],
                              type=request.data['type'], telephone=request.data['telephone'], date_naissance=request.data['date_naissance'], info_authentification=info)
        client.save()

        return Response({"Message": "L'utilisateur a été créé"}, status.HTTP_201_CREATED)


"""
Section API pour client en BAS
"""


class ClientProfile(generics.RetrieveAPIView):
    """API de gestion d'un client """
    serializer_class = serializers.ClientSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    permission_classes = (IsAuthenticated, )

    """
        GET Method
        Route : client/
        """
    def get_object(self):
        queryset = Client.objects.filter()
        user = self.request.user
        print(user.username)
        info = InfoAuthentification.objects.get(username=user.username)
        return queryset.get(info_authentification=info)


class ClientCompte(generics.RetrieveAPIView):
    serializer_class = serializers.ClientCompteSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    permission_classes = (IsAuthenticated, )

    """
        GET Method
        Route : client/compte
    """
    def get_object(self):
        queryset = Compte.objects.filter()
        user = self.request.user
        info = InfoAuthentification.objects.get(username=user.username)
        client = Client.objects.get(info_authentification=info)
        return queryset.get(id=client.id)


class ClientCompteCredit(generics.RetrieveAPIView):
    serializer_class = serializers.ClientCreditSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    permission_classes = (IsAuthenticated, )

    """
        GET Method
        Route : client/compte/credit
    """
    def get_object(self):
        queryset = Credit.objects.filter()
        user = self.request.user
        info = InfoAuthentification.objects.get(username=user.username)
        client = Client.objects.get(info_authentification=info)
        print(client.id)
        return queryset.get(client_id=client.id)


class ClientCompteCourant(generics.RetrieveAPIView):
    serializer_class = serializers.ClientCourantSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    permission_classes = (IsAuthenticated, )

    """
        GET Method
        Route : client/compte/courant
    """
    def get_object(self):
        queryset = Courant.objects.filter()
        user = self.request.user
        info = InfoAuthentification.objects.get(username=user.username)
        client = Client.objects.get(info_authentification=info)
        return queryset.get(client_id=client.id)


class ClientAdresse(generics.RetrieveAPIView):
    serializer_class = serializers.AdresseSerializer
    filter_backends = (filters.DjangoFilterBackend, )
    permission_classes = (IsAuthenticated, )

    """
        GET Method
        Route : client/adresse
    """
    def get_object(self):
        queryset = Adresse.objects.filter()
        user = self.request.user
        info = InfoAuthentification.objects.get(username=user.username)
        client = Client.objects.get(info_authentification=info)
        return queryset.get(client=client.id)
