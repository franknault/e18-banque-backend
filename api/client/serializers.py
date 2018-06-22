from rest_framework import serializers

from api.models import Adresse, Client, Compte, Courant, CarteCredit, Credit, Transaction, TypeTransaction


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class AdresseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adresse
        fields = '__all__'


class ClientsAdresseSerializer(serializers.ModelSerializer):
    adresses = AdresseSerializer(many=True)

    class Meta:
        model = Adresse
        fields = '__all__'
