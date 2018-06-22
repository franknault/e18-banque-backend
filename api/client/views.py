from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from . import serializers
from api.models import *
from django_filters import rest_framework as filters


class ClientsList(generics.ListAPIView):
    queryset = Client.objects.all()
    serializer_class = serializers.ClientSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    permission_classes = (IsAdminUser,)

    #@IsAdminUser
    def get(self, request, *args, **kwargs):
        return self.get(self, request, *args, **kwargs)


class ClientsId(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = serializers.ClientSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    permission_classes = (IsAdminUser, IsAuthenticated)

    #@IsAuthenticated
    def get_queryset(self):
        return Client.objects.filter(pk=self.kwargs['pk'])

    #@IsAdminUser
    def put(self, request, *args, **kwargs):
        return self.put(request, *args, **kwargs)

    #@IsAdminUser
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ClientsIdAdresses(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = serializers.ClientsAdresseSerializer
    filter_backends = (filters.DjangoFilterBackend, )
    permission_classes = (IsAdminUser, IsAuthenticated, )

    #@IsAuthenticated
    def get_queryset(self):
        return Client.objects.filter()

    #@IsAdminUser
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    #@IsAdminUser
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ClientsIdCompte(generics.RetrieveAPIView):
    serializer_class = serializers.ClientsAdresseSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    permission_classes = (IsAdminUser, IsAuthenticated,)

    def get_queryset(self):
        query_courant = Courant.objects.filter()

class ClientIdCompteId(generics.RetrieveAPIView):
