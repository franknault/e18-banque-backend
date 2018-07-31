from rest_framework import serializers

from api.models import *


class TransfertVirementSerializer(serializers.Serializer):
    cpt_prov = serializers.CharField(min_length=8, max_length=8)
    cpt_dest = serializers.CharField(min_length=8, max_length=8)
    montant = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0.00)
    cle_api = serializers.CharField()


class TransfertRemboursementSerializer(serializers.Serializer):
    crt_num_dest = serializers.CharField(min_length=16, max_length=16)
    crt_exp_dest = serializers.CharField(min_length=5, max_length=5)
    crt_cvv_dest = serializers.CharField(min_length=3, max_length=3)
    crt_num_prov = serializers.CharField(min_length=16, max_length=16)
    crt_exp_prov = serializers.CharField(min_length=5, max_length=5)
    crt_cvv_prov = serializers.CharField(min_length=3, max_length=3)
    montant = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0.00)


class TransfertPaiementSerializer(serializers.Serializer):
    cpt_prov = serializers.CharField(min_length=8, max_length=8)
    cpt_dest = serializers.CharField(min_length=8, max_length=8)
    montant = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0.00)


class TransfertAchatSerializer(serializers.Serializer):
    crt_num = serializers.CharField(min_length=16, max_length=16)
    crt_exp = serializers.CharField(min_length=5, max_length=5)
    crt_cvv = serializers.CharField(min_length=3, max_length=3)
    montant = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0.00)
    cle_api = serializers.CharField()
    num_compte = serializers.CharField(min_length=8, max_length=8)


class TransfertStateSerializer(serializers.Serializer):
    cle_api = serializers.CharField()
    etat = serializers.ChoiceField(choices=[Transaction.ACCEPTE, Transaction.REFUSE])


class TransactionListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = '__all__'
