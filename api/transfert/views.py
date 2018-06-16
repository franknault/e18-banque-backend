from rest_framework import generics, status
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from decimal import Decimal
from datetime import datetime

from .serializers import *


class TransfertVirement(generics.CreateAPIView):

    def post(self, request, *args, **kwargs):
        type_trx = TypeTransaction.objects.get(type=TypeTransaction.VIREMENTDEBITDEBIT)
        serializer = TransfertVirementSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({'Détail':'Le body de la requête est invalide.'}, status.HTTP_400_BAD_REQUEST)

        cpt_dest = serializer.data['cpt_dest']
        cpt_prov = serializer.data['cpt_prov']
        montant = Decimal(serializer.data['montant'])

        if cpt_dest == cpt_prov:
            return Response({'Détail':'Le compte de destination ne peut être identique au compte de provenance.'}, status.HTTP_400_BAD_REQUEST)

        if not Courant.objects.filter(num_compte=cpt_dest).exists() or not Courant.objects.filter(num_compte=cpt_prov).exists():
            return Response({'Détail':'Compte de destination ou de provenance introuvable.'}, status.HTTP_400_BAD_REQUEST)

        cpt_prov = Courant.objects.get(num_compte=cpt_prov)
        cpt_dest = Courant.objects.get(num_compte=cpt_dest)

        if not cpt_prov.has_enough_solde(montant=montant):
            return Response({'Détail':'Solde insuffisant dans le compte de provenance'}, status.HTTP_400_BAD_REQUEST)

        id_trx = init_transaction(cpt_prov, cpt_dest, montant, type_trx)

        return Response({'ID': id_trx}, status.HTTP_201_CREATED)


class TransfertPaiement(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        type_trx = TypeTransaction.objects.get(type=TypeTransaction.PAIEMENTDEDEBITACREDIT)
        return Response({"message": "Transfert Débit à Crédit"})


class TransfertAchat(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        type_trx = TypeTransaction.objects.get(type=TypeTransaction.ACHATCREDITADEBIT)
        serializer = TransfertAchatSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({'Détail':'Le body de la requête est invalide.'}, status.HTTP_400_BAD_REQUEST)

        montant = Decimal(serializer.data['montant'])

        try:
            cpt_prov = CarteCredit.objects.get(num_carte=serializer.data['crt_num']).credit
            cpt_dest = Courant.objects.get(num_compte=serializer.data['num_compte'])
        except ObjectDoesNotExist:
            return Response({'Détail':'Le compte de provenance ou de destination est introuvable.'}, status.HTTP_400_BAD_REQUEST)

        if cpt_prov.num_compte == cpt_dest.num_compte:
            return Response({'Détail':'Le compte de destination ne peut être identique au compte de provenance.'})

        if not cpt_prov.carte_credit.validate(exp=serializer.data['crt_exp'], cvv=serializer.data['crt_cvv']):
            return Response({'Détail':'Les informations d\'identification de la carte de crédit sont invalide (expiration et/ou cvv'}, status.HTTP_400_BAD_REQUEST)

        if not cpt_prov.has_enough_credit(montant=montant):
            return Response({'Détail':'Solde insuffisant dans le compte de provenance'})

        # id_trx = init_transaction(cpt_prov, cpt_dest, montant, type_trx)

        return Response({"ID": 10}, status.HTTP_201_CREATED)


class TransfertRemboursement(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        type_trx = TypeTransaction.objects.get(type=TypeTransaction.REMBOURSEMENTCREDITACREDIT)
        serializer = TransfertRemboursementSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({'Détail': 'Le body de la requête est invalide.'}, status.HTTP_400_BAD_REQUEST)

        crt_num_dest = serializer.data['crt_num_dest']
        crt_exp_dest = serializer.data['crt_exp_dest']
        crt_cvv_dest = serializer.data['crt_cvv_dest']
        crt_num_prov = serializer.data['crt_num_prov']
        crt_exp_prov = serializer.data['crt_exp_prov']
        crt_cvv_prov = serializer.data['crt_cvv_prov']
        montant = Decimal(serializer.data['montant'])

        if crt_num_dest == crt_num_prov:
            return Response({'Détail':'Le numéro de carte de destination ne peut être identique au numéro de carte de provenance.'}, status.HTTP_400_BAD_REQUEST)

        if not CarteCredit.objects.filter(num_carte=crt_num_prov).exists() or not CarteCredit.objects.filter(num_carte=crt_num_dest).exists():
            return Response({'Détail':'Compte de destination ou de provenance introuvable.'}, status.HTTP_400_BAD_REQUEST)

        cpt_prov = CarteCredit.objects.get(num_carte=crt_num_prov).credit
        cpt_dest = CarteCredit.objects.get(num_carte=crt_num_dest).credit

        # if not cpt_

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

        return Response({'Détail':'La transaction a déjà été accepté ou refusé.'}, status.HTTP_403_FORBIDDEN)

def init_transaction(cpt_prov, cpt_dest, montant, type_trx):
    trx_prov = Transaction.objects.create(type_transaction=type_trx,
                                          compte=cpt_prov,
                                          montant=montant.copy_negate(),
                                          solde_avant=cpt_prov.solde,
                                          solde_apres=cpt_prov.solde - montant,
                                          etat=Transaction.GELE)

    trx_dest = Transaction.objects.create(type_transaction=type_trx,
                                          compte=cpt_dest,
                                          trx_id=trx_prov.id,
                                          montant=montant,
                                          solde_avant=cpt_dest.solde,
                                          solde_apres=cpt_dest.solde + montant,
                                          etat=Transaction.GELE)

    trx_prov.trx = trx_dest
    trx_prov.save()
    return id