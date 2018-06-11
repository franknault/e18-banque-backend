from rest_framework import generics, status
from rest_framework.response import Response

from api.models import *
from . import serializers


class Comptes(generics.ListCreateAPIView):
    serializer_class = serializers.CompteBasicSerializer

    def get_queryset(self):
        return Compte.objects.filter()

    def post(self, request, *args, **kwargs):
        return Response({'message':'Création d\'un compte'}, status.HTTP_200_OK)


class ComptesId(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.CompteBasicSerializer

    def get_queryset(self):
        return Compte.objects.filter()

    def patch(self, request, *args, **kwargs):
        return Response({'message': 'Changement d\' un élément sur un compte'}, status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        return Response({'message': 'Suppression d\'un compte'}, status.HTTP_200_OK)


class ComptesIdTransaction(generics.ListAPIView):
    serializer_class = serializers.CompteBasicSerializer

    def get_queryset(self):
        return Compte.objects.filter()