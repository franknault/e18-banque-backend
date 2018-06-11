from rest_framework import serializers

from api.models import *


class CompteBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compte
        fields = '__all__'

