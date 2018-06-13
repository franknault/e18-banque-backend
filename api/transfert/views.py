from rest_framework import generics, status
from rest_framework.response import Response
from decimal import Decimal

from api.models import *
from .serializers import TransfertBasicSerializer


class TransfertVirement(generics.CreateAPIView):

    def post(self, request, *args, **kwargs):
        type_trx = TypeTransaction.objects.get(type=TypeTransaction.VIREMENTDEBITDEBIT)

        serializer = TransfertBasicSerializer(data=request.data)
        print(serializer.is_valid())
        body = request.data
        if not body:
            return Response({'Détail':'Veuillez fournir les informations nécessaires dans le body.'}, status.HTTP_400_BAD_REQUEST)

        if not Courant.objects.filter(num_compte=body['compte_destinataire']).exists() or not Courant.objects.filter(num_compte=body['compte_provenance']).exists():
            return Response({'Détail':'Compte de destination ou de provenance introuvable.'}, status.HTTP_400_BAD_REQUEST)

        cpt_prov = Courant.objects.filter(num_compte=body['compte_destinataire']).first()
        cpt_dest = Courant.objects.filter(num_compte=body['compte_provenance']).first()

        if not cpt_prov.has_enough_sold(body['montant']):
            return Response({'Détail':'Solde insuffisant dans le compte de provenance'}, status.HTTP_400_BAD_REQUEST)

        if Transaction.objects.filter(id_transfert=body['id_transfert']).exists():
            return Response({'Détail':'Un transfert existe déjà pour cet ID.'}, status.HTTP_400_BAD_REQUEST)

        trx_prov = Transaction.objects.create(id_transfert=body['id_transfert'],
                                              type_transaction=type_trx,
                                              compte=cpt_prov,
                                              montant=-body['montant'],
                                              solde_avant=cpt_prov.solde,
                                              solde_apres=cpt_prov.solde-Decimal(body['montant']),
                                              etat=Transaction.GELE)

        trx_dest = Transaction.objects.create(id_transfert=body['id_transfert'],
                                              type_transaction=type_trx,
                                              compte=cpt_dest,
                                              trx_id=trx_prov.id,
                                              montant=body['montant'],
                                              solde_avant=cpt_dest.solde,
                                              solde_apres=cpt_dest.solde-Decimal(body['montant']),
                                              etat=Transaction.GELE)
        trx_prov.trx_id = trx_dest.id
        trx_prov.save()
        transactions = Transaction.objects.filter(id_transfert=body['id_transfert'])
        serializer_class = TransfertBasicSerializer(transactions, many=True)

        return Response(serializer.data)



class TransfertPaiement(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        return Response({"message": "Transfert Débit à Crédit"})

class TransfertAchat(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        return Response({"message": "Transfert Crédit à Débit"})

class TransfertRemboursement(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        return Response({"message": "Transfert Crédit à Crédit"})



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