from rest_framework import serializers

from api.models import *


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class ClientSerializerNom(serializers.ModelSerializer):
    prenom_particulier = serializers.CharField(min_length=1, max_length=50, allow_null=True, allow_blank=True)
    nom_particulier = serializers.CharField(min_length=1, max_length=50, allow_null=True, allow_blank=True)
    nom_entreprise = serializers.CharField(min_length=1, max_length=50, allow_null=True, allow_blank=True)
    numero_entreprise = serializers.CharField(min_length=1, max_length=50, allow_null=True, allow_blank=True)
    telephone = serializers.CharField(min_length=8, max_length=11, allow_null=True, allow_blank=True)
    type = serializers.CharField(max_length=1, allow_null=True, allow_blank=True)
    sexe = serializers.CharField(max_length=1, allow_null=True, allow_blank=True)
    date_naissance = serializers.DateField(allow_null=True)
    username = serializers.CharField(min_length=1, max_length=50, allow_null=True, allow_blank=True)
    password = serializers.CharField(min_length=1, max_length=50, allow_null=True, allow_blank=True)
    email = serializers.CharField(min_length=1, max_length=50, allow_null=True, allow_blank=True)
    info_authentification = serializers.IntegerField(allow_null=True)

    class Meta:
        model = Client
        fields = '__all__'


class ClientEntreprise(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id', 'telephone', 'nom_entreprise', 'numero_entreprise')


class ClientParticulier(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id', 'telephone', 'nom_particulier', 'prenom_particulier', 'sexe')
