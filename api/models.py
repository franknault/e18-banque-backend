from django.db import models

# Create your models here.


class Adresse(models.Model):
    pk_adresse = models.AutoField(primary_key=True)
    no_civique = models.CharField(max_length=30)
    nom_rue = models.CharField(max_length=50)
    code_postal = models.CharField(max_length=6)
    ville = models.CharField(max_length=50)
    pays = models.CharField(max_length=50)
    client = models.ForeignKey('Client', on_delete=models.CASCADE)

    @property
    def full_address(self):
        "Return the full address"
        return '%s %s, %s, %s, %s' % (self.no_civique, self.nom_rue, self.code_postal, self.ville, self.pays)

    class Meta:
        db_table = 'adresse'
        verbose_name = 'adresse'
        verbose_name_plural = 'adresses'


class Client(models.Model):
    HOMME = 'H'
    FEMME = 'F'
    AUCUN = 'A'
    SEXE_CHOICES = (
        (HOMME, 'Homme'),
        (FEMME, 'Femme'),
        (AUCUN, 'Non défini'),
    )

    ENTREPRISE = 'E'
    PARTICULIER = 'P'
    TYPE_CHOICES = (
        (ENTREPRISE, 'Entreprise'),
        (PARTICULIER, 'Particulier'),
    )

    pk_client = models.AutoField(primary_key=True)
    courriel = models.EmailField()
    telephone = models.CharField(max_length=11)
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    nom_particulier = models.CharField(max_length=50, null=True, blank=True)
    prenom_particulier = models.CharField(max_length=50, null=True, blank=True)
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES, null=True, blank=True)
    date_naissance = models.DateField(null=True, blank=True)
    nom_entreprise = models.CharField(max_length=50, null=True, blank=True)
    numero_entreprise = models.CharField(max_length=50, null=True, blank=True)

    @property
    def full_name(self):
        "Return the full name"
        if self.nom_particulier and self.prenom_particulier:
            return '%s %s' % (self.prenom_particulier, self.nom_particulier)
        elif self.nom_entreprise and self.numero_entreprise:
            return '%s, %s' % (self.nom_entreprise, self.numero_entreprise)

    class Meta:
        db_table = 'client'
        verbose_name = 'client'
        verbose_name_plural = 'clients'


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
    