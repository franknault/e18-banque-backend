from django.db import models

# Create your models here.

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


class Courant(models.Model):
    first_name = models.CharField(max_length=30)


class Credit(models.Model):
    limite = models.DecimalField(max_digits=10, decimal_places=2)


class Compte(models.Model):
    solde = models.DecimalField(max_digits=10, decimal_places=2)
    num_compte = models.CharField(max_length=8)
    date_ouverture = models.DateTimeField(auto_now_add=True)
    date_fermeture = models.DateTimeField()


class CarteCredit(models.Model):
    nom_titulaire = models.CharField(max_length=100)
    num_carte = models.CharField(max_length=100)
    annee_expiration = models.CharField(max_length=2)
    mois_expiration = models.CharField(max_length=2)
    cvv = models.CharField(max_length=3)
    date_emission = models.DateTimeField(auto_now_add=True)



class Transaction(models.Model):
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_debut = models.DateTimeField(auto_now_add=True)
    date_fin = models.DateTimeField()
    etat = models.CharField(max_length=3)
    