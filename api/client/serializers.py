from rest_framework import serializers

from api.models import Adresse, Client, Compte, Courant, CarteCredit, Credit, Transaction, TypeTransaction


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


class AdresseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adresse
        fields = '__all__'


class ClientsAdresseSerializer(serializers.ModelSerializer):
    adresses = AdresseSerializer(many=True)

    class Meta:
        model = Adresse
        fields = '__all__'
