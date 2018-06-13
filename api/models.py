from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import MinValueValidator


class InfoAuthentification(AbstractUser):
    id = models.AutoField(primary_key=True)


class Administrateur(models.Model):
    id = models.AutoField(primary_key=True)
    info_authentification = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


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

    id = models.AutoField(primary_key=True)
    info_authentification = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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


class Adresse(models.Model):
    id = models.AutoField(primary_key=True)
    no_civique = models.CharField(max_length=30)
    nom_rue = models.CharField(max_length=50)
    code_postal = models.CharField(max_length=6)
    ville = models.CharField(max_length=100)
    pays = models.CharField(max_length=100)
    client = models.ForeignKey(Client, related_name='adresses', on_delete=models.CASCADE)

    @property
    def full_address(self):
        "Return the full address"
        return '%s %s, %s, %s, %s' % (self.no_civique, self.nom_rue, self.code_postal, self.ville, self.pays)

    class Meta:
        db_table = 'adresse'
        verbose_name = 'adresse'
        verbose_name_plural = 'adresses'


class Session(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.OneToOneField(Client, on_delete=models.CASCADE)
    est_connecte = models.BooleanField
    est_valide = models.BooleanField
    token = models.CharField(max_length=512, null=True, blank=True)


class Compte(models.Model):
    id = models.AutoField(primary_key=True)
    num_compte = models.CharField(max_length=8, unique=True)
    solde = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.00)])
    date_ouverture = models.DateTimeField(auto_now_add=True)
    date_fermeture = models.DateTimeField(null=True)

    def has_enough_sold(self, montant):
        return self.solde.__ge__(montant)

    class Meta:
        db_table = 'compte'


class Courant(Compte):
    courant_id = models.AutoField(primary_key=True)
    client = models.OneToOneField(Client, on_delete=models.CASCADE)

    class Meta:
        db_table = 'courant'


class CarteCredit(models.Model):
    id = models.AutoField(primary_key=True)
    nom_titulaire = models.CharField(max_length=200)
    num_carte = models.CharField(max_length=100, unique=True)
    annee_expiration = models.CharField(max_length=2)
    mois_expiration = models.CharField(max_length=2)
    cvv = models.CharField(max_length=255)
    date_emission = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cartecredit'


class Credit(Compte):
    credit_id = models.AutoField(primary_key=True)
    client = models.OneToOneField(Client, on_delete=models.CASCADE)
    carte_credit = models.OneToOneField(CarteCredit, on_delete=models.CASCADE)
    limite = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'credit'


class TypeTransaction(models.Model):
    VIREMENTDEBITDEBIT = 'VMT'
    PAIEMENTDEDEBITACREDIT = 'PMT'
    ACHATCREDITADEBIT = 'ACT'
    REMBOURSEMENTCREDITACREDIT = 'RBT'
    TYPE_CHOICES = (
        (VIREMENTDEBITDEBIT, 'Virement debit-debit'),
        (PAIEMENTDEDEBITACREDIT, 'Paiement debit-credit'),
        (ACHATCREDITADEBIT, 'Achat credit-debit'),
        (REMBOURSEMENTCREDITACREDIT, 'Remboursement credit-credit'),
    )

    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    description = models.TextField()

    class Meta:
        db_table = 'type_transaction'


class Transaction(models.Model):
    ACCEPTE = 'ACC'
    REFUSE = 'REF'
    GELE = 'GEL'
    ETAT_CHOICES = (
        (ACCEPTE, 'Acceptée'),
        (REFUSE, 'Refusée'),
        (GELE, 'Gelée'),
    )

    id = models.AutoField(primary_key=True)
    type_transaction = models.ForeignKey(TypeTransaction, on_delete=models.DO_NOTHING)
    compte = models.ForeignKey(Compte, related_name='transactions', on_delete=models.DO_NOTHING)
    trx = models.OneToOneField('self', related_name='transaction', on_delete=models.DO_NOTHING, null=True)
    date_debut = models.DateTimeField(auto_now_add=True)
    date_fin = models.DateTimeField(null=True)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    solde_avant = models.DecimalField(max_digits=10, decimal_places=2)
    solde_apres = models.DecimalField(max_digits=10, decimal_places=2)
    etat = models.CharField(max_length=3, choices=ETAT_CHOICES)

    class Meta:
        db_table = 'transaction'
