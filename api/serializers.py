from rest_framework import serializers

from .models import Adresse, Client, Compte, Courant, CarteCredit, Credit, Transaction, TypeTransaction


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class ClientEntreprise(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id', 'telephone', 'nom_entreprise', 'numero_entreprise')


class ClientParticulier(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id', 'telephone', 'nom_particulier', 'prenom_particulier', 'sexe')
