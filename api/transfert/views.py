from rest_framework import generics, status
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from decimal import Decimal
from datetime import datetime
from django.conf import settings
from django.utils import timezone
from django.utils.timezone import localtime
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import *


class TransfertVirement(generics.CreateAPIView):
    """ API de création d'un virement, un transfert d'un compte débit vers un compte débit """
    permission_classes = (AllowAny,)

    """
    POST Methode
    Route : transfert/virement
    """
    def post(self, request, *args, **kwargs):
        type_trx = TypeTransaction.objects.get(type=TypeTransaction.VIREMENTDEBITDEBIT)
        serializer = TransfertVirementSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({'Détail': 'Le body de la requête est invalide.'}, status.HTTP_400_BAD_REQUEST)

        cpt_dest = serializer.data['cpt_dest']
        cpt_prov = serializer.data['cpt_prov']
        montant = Decimal(serializer.data['montant'])
        api_key = serializer.data['cle_api']

        if api_key != settings.ANALYTIQUE_API_KEY:
            return Response({"Message": "Vous n'êtes pas autorisé à modifier cette transaction."}, status.HTTP_401_UNAUTHORIZED)

        if cpt_dest == cpt_prov:
            return Response({'Détail': 'Le compte de destination ne peut être identique au compte de provenance.'}, status.HTTP_400_BAD_REQUEST)

        if not Courant.objects.filter(num_compte=cpt_dest).exists() or not Courant.objects.filter(num_compte=cpt_prov).exists():
            return Response({'Détail': 'Compte de destination ou de provenance introuvable.'}, status.HTTP_400_BAD_REQUEST)


        cpt_prov = Courant.objects.get(num_compte=cpt_prov)
        cpt_dest = Courant.objects.get(num_compte=cpt_dest)

        if not cpt_prov.has_enough_solde(montant=montant):
            return Response({'Détail': 'Solde insuffisant dans le compte de provenance'}, status.HTTP_400_BAD_REQUEST)

        trx_prov = Transaction.objects.create(type_transaction=type_trx,
                                              compte=cpt_prov,
                                              montant=montant.copy_negate(),
                                              solde_avant=cpt_prov.solde,
                                              solde_apres=cpt_prov.solde - montant,
                                              etat=Transaction.ACCEPTE)

        cpt_prov.solde = trx_prov.solde_apres
        cpt_prov.save()

        trx_dest = Transaction.objects.create(type_transaction=type_trx,
                                              compte=cpt_dest,
                                              trx_id=trx_prov.id,
                                              montant=montant,
                                              solde_avant=cpt_dest.solde,
                                              solde_apres=cpt_dest.solde + montant,
                                              etat=Transaction.ACCEPTE)

        trx_prov.trx = trx_dest
        trx_prov.save()

        cpt_dest.solde = trx_dest.solde_apres
        cpt_dest.save()

        return Response({'ID': trx_prov.id}, status.HTTP_201_CREATED)


class TransfertPaiement(generics.CreateAPIView):
    """ API de création d'un paiement, un transfert d'un compte débit vers un compte crédit """

    """
    POST Methode
    Route : transfert/paiement
    """
    def post(self, request, *args, **kwargs):
        type_trx = TypeTransaction.objects.get(type=TypeTransaction.PAIEMENTDEDEBITACREDIT)
        return Response({"Message": "Transfert de Débit à Crédit"}, status.HTTP_201_CREATED)


class TransfertAchat(generics.CreateAPIView):
    """ API de création d'un achat, un transfert d'un compte crédit vers un compte débit """

    permission_classes = (AllowAny,)

    """
    POST Methode
    Route : tranfert/achat
    """
    def post(self, request, *args, **kwargs):
        type_trx = TypeTransaction.objects.get(type=TypeTransaction.ACHATCREDITADEBIT)
        serializer = TransfertAchatSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({"Message": "Le body de la requête est invalide."}, status.HTTP_400_BAD_REQUEST)

        montant = Decimal(serializer.data['montant'])
        api_key = serializer.data['cle_api']

        try:
            cpt_prov = CarteCredit.objects.get(num_carte=serializer.data['crt_num']).credit
            cpt_dest = Courant.objects.get(num_compte=serializer.data['num_compte'])
        except ObjectDoesNotExist:
            return Response({"Message": "Le compte de provenance ou de destination est introuvable."}, status.HTTP_404_NOT_FOUND)

        if cpt_prov.num_compte == cpt_dest.num_compte:
            return Response({"Message": "Le compte de destination ne peut être identique au compte de provenance."}, status.HTTP_412_PRECONDITION_FAILED)

        if api_key != settings.PASSERELLE_API_KEY:
            return Response({"Message": "Vous n'êtes pas autorisé à modifier cette transaction."}, status.HTTP_401_UNAUTHORIZED)

        if not cpt_prov.carte_credit.validate(exp=serializer.data['crt_exp'], cvv=serializer.data['crt_cvv']):
            return Response({"Message": "Les informations d'identification de la carte de crédit sont invalides (expiration et/ou cvv)"}, status.HTTP_417_EXPECTATION_FAILED)

        if not cpt_prov.has_enough_credit(montant=montant):
            return Response({"Message": "Solde insuffisant dans le compte de provenance."}, status.HTTP_412_PRECONDITION_FAILED)

        trx_prov = Transaction.objects.create(type_transaction=type_trx,
                                              compte=cpt_prov,
                                              montant=montant.copy_negate(),
                                              solde_avant=cpt_prov.solde,
                                              solde_apres=cpt_prov.solde + montant,
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

        return Response({"ID": trx_prov.id}, status.HTTP_201_CREATED)


class TransfertRemboursement(generics.CreateAPIView):
    """ API de création d'un remboursement, un transfert d'un compte crédit vers un compte crédit """

    """
    POST Methode
    Route : transfert/remboursement
    """
    def post(self, request, *args, **kwargs):
        type_trx = TypeTransaction.objects.get(type=TypeTransaction.REMBOURSEMENTCREDITACREDIT)
        return Response({"Message": "Transfert de Crédit à Crédit"}, status.HTTP_201_CREATED)


class TransfertState(generics.RetrieveUpdateAPIView):
    """ API de gestion de transfert. Permet un vérification et un changement d'état : REF ou ACC """

    serializer_class = TransactionListSerializer
    permission_classes = (AllowAny,)

    """
    GET Methode
    Route : transfert/:id
    """
    def get_queryset(self):

        return Transaction.objects.filter()

    """
    PATCH Methode
    Route : transfert/:id
    """
    def patch(self, request, *args, **kwargs):
        serializer = TransfertStateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({"Message": "Le body de la requête est invalide."}, status.HTTP_400_BAD_REQUEST)

        etat = request.data['etat']
        api_key = request.data['cle_api']

        try:
            trx = Transaction.objects.get(pk=self.kwargs['pk'])
            trx_dest = Transaction.objects.get(pk=trx.transaction.id)
        except Transaction.DoesNotExist:
            return Response({"Message": "La transaction avec l'id: {} n'existe pas".format(kwargs['pk'])}, status.HTTP_404_NOT_FOUND)

        if trx.type_transaction != 3 and api_key != settings.PASSERELLE_API_KEY:
            return Response({"Message": "Vous n'êtes pas autorisé à modifier cette transaction."}, status.HTTP_401_UNAUTHORIZED)

        if trx.etat == Transaction.ACCEPTE and trx.etat == Transaction.REFUSE:
            return Response({"Message": "La transaction a déjà été accepté ou refusé."}, status.HTTP_412_PRECONDITION_FAILED)

        trx.date_fin = localtime(timezone.now())
        trx.etat = etat
        trx.save()
        trx_dest.date_fin = localtime(timezone.now())
        trx_dest.etat = etat
        trx_dest.save()

        return Response({"Message": "L'état de la transaction a été changé pour : {}".format(request.data['etat'])}, status.HTTP_200_OK)
