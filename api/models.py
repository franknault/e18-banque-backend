from django.db import models


class Adresse(models.Model):
    no_civique = models.CharField(max_length=30)
    nom_rue = models.CharField(max_length=50)
    code_postal = models.CharField(max_length=6)
    ville = models.CharField(max_length=50)
    pays = models.CharField(max_length=50)


class Client(models.Model):
    courriel = models.EmailField()
    telephone = models.CharField(max_length=11)
    type = models.CharField(max_length=1)
    nom_particulier = models.CharField(max_length=50)
    prenom_particulier = models.CharField(max_length=50)
    sexe = models.CharField(max_length=1)
    date_naissance = models.DateField()
    nom_entreprise = models.CharField(max_length=50)
    numero_entreprise = models.CharField(max_length=50)


class CarteCredit(models.Model):
    pk_carte_Credit_id = models.AutoField(primary_key=True)
    nom_titulaire = models.CharField(max_length=100)
    num_carte = models.CharField(max_length=100, unique=True)
    annee_expiration = models.CharField(max_length=2)
    mois_expiration = models.CharField(max_length=2)
    cvv = models.CharField(max_length=512)
    date_emission = models.DateTimeField(auto_now_add=True)


class Compte(models.Model):
    pk_compte_id = models.AutoField(primary_key=True)
    num_compte = models.CharField(max_length=8, unique=True)
    solde = models.DecimalField(max_digits=10, decimal_places=2)
    date_ouverture = models.DateTimeField(auto_now_add=True)
    date_fermeture = models.DateTimeField(null=True)


class Courant(Compte):
    pk_compte_id = models.AutoField(primary_key=True)
    fk_client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    fk_compte_id = models.ForeignKey(Compte, on_delete=models.CASCADE)


class Credit(Compte):
    pk_compte_id = models.AutoField(primary_key=True)
    fk_compte_id = models.ForeignKey(Compte, on_delete=models.CASCADE)
    fk_client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    fk_carte_Credit_id = models.ForeignKey(CarteCredit, on_delete=models.CASCADE)
    limite = models.DecimalField(max_digits=10, decimal_places=2)


class TypeTransaction(models.Model):
    pk_type_transaction_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50)


class Transaction(models.Model):
    pk_transaction_id = models.AutoField(primary_key=True)
    fk_type_transaction_id = models.ForeignKey(TypeTransaction, on_delete=models.DO_NOTHING)
    fk_compte_id = models.ForeignKey(Compte, on_delete=models.DO_NOTHING)
    fk_transaction_id = models.ForeignKey('self', on_delete=models.DO_NOTHING)
    date_debut = models.DateTimeField(auto_now_add=True)
    date_fin = models.DateTimeField(null=True)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    solde_avant = models.DecimalField(max_digits=10, decimal_places=2)
    solde_apres = models.DecimalField(max_digits=10, decimal_places=2)
    etat = models.CharField(max_length=3)