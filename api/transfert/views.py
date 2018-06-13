from rest_framework import generics, status
from rest_framework.response import Response
from decimal import Decimal
from datetime import datetime

from .serializers import *


class TransfertVirement(generics.CreateAPIView):

    def post(self, request, *args, **kwargs):
        type_trx = TypeTransaction.objects.get(type=TypeTransaction.VIREMENTDEBITDEBIT)
        serializer = TransfertBasicSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({'Détail':'Le body de la requête est invalide.'}, status.HTTP_400_BAD_REQUEST)

        cpt_dest = serializer.data['compte_destinataire']
        cpt_prov = serializer.data['compte_provenance']
        montant = Decimal(serializer.data['montant'])

        if cpt_dest == cpt_prov:
            return Response({'Détail':'Le compte de destination ne peut être identique au compte de provenance.'}, status.HTTP_400_BAD_REQUEST)

        if not Courant.objects.filter(num_compte=cpt_dest).exists() or not Courant.objects.filter(num_compte=cpt_prov).exists():
            return Response({'Détail':'Compte de destination ou de provenance introuvable.'}, status.HTTP_400_BAD_REQUEST)

        cpt_prov = Courant.objects.filter(num_compte=cpt_prov).first()
        cpt_dest = Courant.objects.filter(num_compte=cpt_dest).first()

        if not cpt_prov.has_enough_sold(montant=montant):
            return Response({'Détail':'Solde insuffisant dans le compte de provenance'}, status.HTTP_400_BAD_REQUEST)

        trx_prov = Transaction.objects.create(type_transaction=type_trx,
                                              compte=cpt_prov,
                                              montant=montant.copy_negate(),
                                              solde_avant=cpt_prov.solde,
                                              solde_apres=cpt_prov.solde-montant,
                                              etat=Transaction.GELE)

        trx_dest = Transaction.objects.create(type_transaction=type_trx,
                                              compte=cpt_dest,
                                              trx_id=trx_prov.id,
                                              montant=montant,
                                              solde_avant=cpt_dest.solde,
                                              solde_apres=cpt_dest.solde+montant,
                                              etat=Transaction.GELE)

        trx_prov.trx = trx_dest
        trx_prov.save()

        return Response({'Id':trx_prov.id})


class TransfertPaiement(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        type_trx = TypeTransaction.objects.get(type=TypeTransaction.PAIEMENTDEDEBITACREDIT)
        return Response({"message": "Transfert Débit à Crédit"})


class TransfertAchat(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        type_trx = TypeTransaction.objects.get(type=TypeTransaction.ACHATCREDITADEBIT)
        return Response({"message": "Transfert Crédit à Débit"})


class TransfertRemboursement(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        type_trx = TypeTransaction.objects.get(type=TypeTransaction.REMBOURSEMENTCREDITACREDIT)
        return Response({"message": "Transfert Crédit à Crédit"})


class TransfertState(generics.RetrieveUpdateAPIView):
    serializer_class = TransactionListSerializer

    def get_queryset(self):
        return Transaction.objects.filter()

    def patch(self, request, *args, **kwargs):
        if Transaction.objects.get(pk=self.kwargs['pk']).etat != Transaction.ACCEPTE\
                and Transaction.objects.get(pk=self.kwargs['pk']).etat != Transaction.REFUSE:
            trx = Transaction.objects.get(pk=self.kwargs['pk'])
            Transaction.objects.filter(id=trx.transaction.id).update(date_fin=datetime.now(), etat=request.data['etat'])
            Transaction.objects.filter(id=trx.id).update(date_fin=datetime.now())
            return self.partial_update(request, *args, **kwargs)

        return Response({'Détail':'La transaction a déjà été accepté ou refusé.'}, status.HTTP_400_BAD_REQUEST)
