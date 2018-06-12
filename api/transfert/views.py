from rest_framework import generics, status
from rest_framework.response import Response
import json

from api.models import *


class TransfertFreeze(generics.CreateAPIView):

    def post(self, request, *args, **kwargs):
        body = request.data
        if not body:
            return Response({'détail':'Veuillez fournir les informations nécessaires dans le body.'}, status.HTTP_400_BAD_REQUEST)

        if body['type_transfert'] == TypeTransaction.VIREMENTDEBITDEBIT:
            return traiter_virement(self, body)

        if request.data['type_transfert'] == TypeTransaction.PAIEMENTDEDEBITACREDIT:
            return traiter_paiement(self, body)

        if request.data['type_transfert'] == TypeTransaction.ACHATCREDITADEBIT:
            return traiter_achat(self, body)

        if request.data['type_transfert'] == TypeTransaction.REMBOURSEMENTCREDITACREDIT:
            return traiter_remboursement(self, body)


def traiter_virement(self, body):
    if not Courant.objects.filter(num_compte=body['compte_provenance']) or not Courant.objects.filter(num_compte=body['compte_destination']):
        return Response({'Détails':'Le compte de destination et de provenance doivent être des comptes Courant pour une transaction de Virement'})
    return Response({"message": "Transfert Débit à Débit"})

def traiter_paiement(self, body):
    if not Courant.objects.filter(num_compte=body['compte_provenance']) or not Credit.objects.filter(num_compte=body['compte_destination']):
        return Response({'Détails':'Le compte de destination et de provenance doivent être des comptes Courant pour une transaction de Virement'})
    return Response({"message": "Transfert Débit à Crédit"})

def traiter_achat(self, body):
    if not Credit.objects.filter(num_compte=body['compte_provenance']) or not Courant.objects.filter(num_compte=body['compte_destination']):
        return Response({'Détails':'Le compte de destination et de provenance doivent être des comptes Courant pour une transaction de Virement'})
    return Response({"message": "Transfert Crédit à Débit"})

def traiter_remboursement(self, body):
    if not Credit.objects.filter(num_compte=body['compte_provenance']) or not Credit.objects.filter(num_compte=body['compte_destination']):
        return Response({'Détails':'Le compte de destination et de provenance doivent être des comptes Courant pour une transaction de Virement'})
    return Response({"message": "Transfert Crédit à Crédit"})