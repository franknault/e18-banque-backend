from rest_framework import serializers
from api.models import *


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('date_fin', 'montant', 'solde_avant', 'solde_apres', 'etat', 'type_transaction', 'trx',)


class TransactionSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
