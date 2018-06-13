from rest_framework import serializers

from api.models import *


class TransfertBasicSerializer(serializers.Serializer):
    compte_provenance = serializers.CharField()
    compte_destinataire = serializers.CharField()
    montant = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0.00)

class TransfertStateSerializer(serializers.Serializer):
    etat = serializers.ChoiceField(choices=[Transaction.ACCEPTE, Transaction.REFUSE])



class TransactionListSerializer(serializers.ModelSerializer):
    etat = serializers.ChoiceField(choices=[Transaction.ACCEPTE, Transaction.REFUSE])

    class Meta:
        model = Transaction
        fields = '__all__'
