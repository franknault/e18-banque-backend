from rest_framework.generics import ListAPIView
from . import serializers
from .serializers import *
from api.models import *
from . import serializers
from rest_framework.permissions import IsAdminUser
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.mixins import CreateModelMixin


"""class ClientsApi(ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

"""

class ClientsEntrepriseApi(ListAPIView):
    queryset = Client.objects.filter(type=Client.ENTREPRISE).all()
    serializer_class = ClientEntreprise


class ClientsParticulierApi(ListAPIView):
    queryset = Client.objects.filter(type=Client.PARTICULIER).all()
    serializer_class = ClientParticulier


class ClientsApi(CreateAPIView):
    queryset = Client.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = serializers.ClientSerializerNom

    """
    GET Method
    Route : client/
    """

    """
    POST Method
    Route : client/
    """

    def post(self, request, *args, **kwargs):

        info = InfoAuthentification.objects.create_user(username=request.data['username'], email=request.data['email'], password=request.data['password'])
        info.save()

        token = Token.objects.create(user=info)
        token.save()

        request.data['info_authentification'] = info.pk
        client = Client.objects.create(nom_particulier=request.data['nom_particulier'], prenom_particulier=request.data['prenom_particulier'], sexe=request.data['sexe'],
                              nom_entreprise=request.data['nom_entreprise'], numero_entreprise=request.data['numero_entreprise'],
                              type=request.data['type'], telephone=request.data['telephone'], date_naissance=request.data['date_naissance'], info_authentification=info)
        client.save()


        return Response({"Message": "Client est creer :)"})


"""return Response({"Message": "L'utilisateur ne peut être créer."}, status.HTTP_412_PRECONDITION_FAILED)"""
