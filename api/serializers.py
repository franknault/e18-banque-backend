from rest_framework import serializers

from .models import Adresse, Client, Compte, Courant, CarteCredit, Credit, Transaction, TypeTransaction


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'