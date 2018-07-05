from rest_framework import serializers

from api.models import Adresse, Client, Compte, Courant, CarteCredit, Credit, Transaction, TypeTransaction
from api.compte.serializers import CompteBasicSerializer


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
        model = Client
        fields = ('id', 'adresses')


class ClientCourantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courant
        fields = '__all__'


class ClientCreditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credit
        fields = '__all__'


class ClientCompteSerializer(serializers.ModelSerializer):
    courant = ClientCourantSerializer()
    credit = ClientCreditSerializer()

    class Meta:
        model = Compte
        fields = ('id', 'courant', 'credit')
