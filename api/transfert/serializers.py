from rest_framework import serializers

from api.models import *


class TransfertBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'