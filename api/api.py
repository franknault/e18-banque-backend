from rest_framework.generics import ListAPIView

from .serializers import ClientSerializer
from .models import Client


class ClientApi(ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer