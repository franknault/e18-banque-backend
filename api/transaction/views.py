from api.models import *
from . import serializers
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import status
from django.http import JsonResponse
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django_filters import rest_framework as filters


class TransactionsList(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = serializers.TransactionSerializer
    permission_classes = (IsAdminUser, )

    """
    POST Method
    Route : admin/transaction/
    """
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    """
    HEAD Method
    Override the default HEAD method to disable it and to return a French message.
    Route : transaction/
    """

    def head(self, request):
        if request.method == 'HEAD':
            return JsonResponse({'État': "échoué", 'message': "L'opération HEAD n'est pas supporté"}, status=403)

    """
    OPTIONS Method
    Override the default OPTIONS method to disable it and to return a French message.
    Route : transaction/
    """

    def options(self, request):
        if request.method == 'OPTIONS':
            return JsonResponse({'État': "échoué", 'message': "L'opération OPTIONS n'est pas supporté"}, status=403)

    """
    PATCH Method
    Override the default PATCH method to disable it and to return a French message.
    Route : transaction/
    """

    def patch(self, request, *args, **kwargs):
            return Response(
                data={
                    'État': "échoué", 'message': "L'opération PATCH n'est pas supporté"
                },
                status=status.HTTP_404_NOT_FOUND
            )

    """
    PUT Method
    Override the default PUT method to disable it and to return a French message.
    Route : transaction/
    """

    def put(self, request, *args, **kwargs):
            return Response(
                data={
                    'État': "échoué", 'message': "L'opération PUT n'est pas supporté"
                },
                status=status.HTTP_404_NOT_FOUND
            )

    """
    DELETE Method
    Override the default DELETE method to disable it and to return a French message.
    Route : transaction/
    """

    def delete(self, request, *args, **kwargs):
            return Response(
                data={
                    'État': "échoué", 'message': "L'opération DELETE n'est pas supporté"
                },
                status=status.HTTP_404_NOT_FOUND
            )


class TransactionId(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminUser,)
    queryset = Transaction.objects.all()
    serializer_class = serializers.TransactionSerializer

    """
    GET Method
    Route : admin/transaction/:id/
    """

    def get(self, request, *args, **kwargs):
        try:
            transaction = self.queryset.get(pk=kwargs["pk"])
            return Response(serializers.TransactionSerializer(transaction).data)
        except Transaction.DoesNotExist:
            return Response(
                data={
                    "message": "La transaction avec l'id: {} n'existe pas".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    """
    PATCH Method
    Route : transaction/:id/
    """

    def patch(self, request, *args, **kwargs):
        try:
            transaction = self.queryset.get(pk=kwargs["pk"])
            return self.partial_update(request, *args, **kwargs)
        except Transaction.DoesNotExist:
            return Response(
                data={
                    "message": "La transaction avec l'id: {} n'existe pas".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    """
    DELETE Method
    Override the default DELETE method to disable it and to return a French message.
    Route : transaction/:id/
    """
    def destroy(self, request, *args, **kwargs):
        return JsonResponse({'État': "échoué", 'message': "L'opération DELETE n'est pas supporté"}, status=403)

    """
    PUT Method
    Override the default PUT method to disable it and to return a French message.
    Route : transaction/:id/
    """

    def put(self, request, *args, **kwargs):
        return JsonResponse({'État': "échoué", 'message': "L'opération PUT n'est pas supporté"}, status=403)

    """
    POST Method
    Override the default POST method to disable it and to return a French message.
    Route : transaction/:id/
    """

    def post(self, request, *args, **kwargs):
        return JsonResponse({'État': "échoué", 'message': "L'opération POST n'est pas supporté"}, status=403)

    """
    HEAD Method
    Override the default HEAD method to disable it and to return a French message.
    Route : transaction/:id/
    """

    def head(self, request, *args, **kwargs):
        if request.method == 'HEAD':
            return JsonResponse({'État': "échoué", 'message': "L'opération HEAD n'est pas supporté"}, status=403)

    """
    OPTIONS Method
    Override the default OPTIONS method to disable it and to return a French message.
    Route : transaction/:id/
    """

    def options(self, request, *args, **kwargs):
        if request.method == 'OPTIONS':
            return JsonResponse({'État': "échoué", 'message': "L'opération OPTIONS n'est pas supporté"}, status=403)


"""
Section API pour client en BAS
"""


class TransactionCompte(generics.ListAPIView):
    serializer_class = serializers.TransactionSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    permission_classes = (IsAuthenticated,)
    """
            GET Method
            Route : client/transaction
    """
    def get_queryset(self):
        queryset = Transaction.objects.all()
        user = self.request.user
        info = InfoAuthentification.objects.get(username=user.username)
        client = Client.objects.get(info_authentification=info)
        compte = Compte.objects.get(id=client.id)
        return queryset.filter(compte_id=compte.id)
