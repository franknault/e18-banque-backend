from api.models import *
from . import serializers
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import status
from django.http import JsonResponse


class TransactionsList(generics.ListCreateAPIView):

    """
    GET  Method
    Route : transaction/
    """

    queryset = Transaction.objects.all()
    serializer_class = serializers.TransactionSerializer

    """
    POST  Method
    Route : transaction/
    """
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class TransactionId(RetrieveUpdateDestroyAPIView):

    queryset = Transaction.objects.all()
    serializer_class = serializers.TransactionSerializer

    """
    GET Method
    Route : transaction/:id/
    """

    def get(self, request, *args, **kwargs):
        try:
            transaction = self.queryset.get(pk=kwargs["pk"])
            return Response(serializers.TransactionSerializer(transaction).data)
        except Transaction.DoesNotExist:
            return Response(
                data={
                    "message": "Transaction with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    """
    PATCH Method
    Route : transaction/:id/
    """
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    """
    Override the default delete method to disable it 
    Route : transaction/:id/
    """
    def destroy(self, request, *args, **kwargs):
        return JsonResponse({'success': False, 'message': "DELETE not allowed"}, status=403)

    """
    Override the default put method to disable it 
    Route : transaction/:id/
    """

    def put(self, request, *args, **kwargs):
        return JsonResponse({'success': False, 'message': "PUT not allowed"}, status=403)
