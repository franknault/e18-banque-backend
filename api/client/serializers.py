from django.core.serializers import serialize
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
    info_authentification = serializers.CharField(allow_null=True)

    class Meta:
        model = Client
        fields = '__all__'


class AdresseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adresse
        fields = '__all__'


class ClientsAdresseSerializer(serializers.ModelSerializer):
    adresses = AdresseSerializer(many=True)

    class Meta:
        model = Adresse
        fields = ('adresses',  )


class ClientCourantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courant
        fields = '__all__'


class ClientCarteCreditSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarteCredit
        fields = '__all__'


class ClientCreditSerializer(serializers.ModelSerializer):
    carte_credit = ClientCarteCreditSerializer()

    class Meta:
        model = Credit
        fields = ('num_compte', 'solde', 'date_ouverture', 'date_fermeture', 'limite', 'carte_credit')


class ClientCompteSerializer(serializers.ModelSerializer):
    courant = ClientCourantSerializer()
    credit = ClientCreditSerializer()

    class Meta:
        model = Compte
        fields = ('id', 'courant', 'credit')
