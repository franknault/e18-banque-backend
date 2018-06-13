from rest_framework import serializers

from api.models import *


class TransfertBasicSerializer(serializers.Serializer):
    id_transfert = serializers.IntegerField()
    compte_provenance = serializers.CharField()
    compte_destinataire = serializers.CharField()
    montant = serializers.DecimalField(max_digits=10, decimal_places=2)
