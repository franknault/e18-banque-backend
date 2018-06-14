from rest_framework import serializers

from api.models import *
from api.transaction.serializers import TransactionSerializer


class CompteBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compte
        fields = '__all__'


class CompteTransactionSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True)

    class Meta:
        model = Compte
        fields = ('id', 'transactions')
