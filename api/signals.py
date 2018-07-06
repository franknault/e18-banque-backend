from django.db.models.signals import post_save
from django.dispatch import receiver
from api.models import *

from faker import Faker

fake = Faker()


@receiver(post_save, sender=Transaction)
def gel_fond(sender, instance, **kwargs):
    """ Met à jour le solde des comptes lors d'un changement d'état d'une transaction """

    if instance.etat == Transaction.GELE:
        compte = instance.compte
        compte.solde = instance.solde_apres
        compte.save()

    if instance.etat == Transaction.REFUSE:
        if hasattr(instance.compte, 'credit'):
            compte = instance.compte
            compte.solde = compte.solde + instance.montant
            compte.save()
        if hasattr(instance.compte, 'courant'):
            compte = instance.compte
            compte.solde = compte.solde - instance.montant
            compte.save()


@receiver(post_save, sender=Credit)
@receiver(post_save, sender=Courant)
def update_num_compte(sender, instance, created, **kwargs):
    """ Initialise le numéro de compte selon l'id lors de la création """

    if created:
        prefix = 'NRB'
        num = prefix + format(instance.id, '05')
        Compte.objects.filter(id=instance.id).update(num_compte=num)


@receiver(post_save, sender=Client)
def generate_compte(sender, instance, **kwargs):
    """ Génère les comptes lors de la création d'un client """

    client = Client.objects.get(id=instance.id)
    create_courant(client)
    create_credit(client)


def create_courant(client):
    """ Crée un compte Courant de base """

    Courant.objects.create(solde=0.00, client=client)


def create_credit(client):
    """ Initialise une carte de crédit et crée le compte Crédit """

    card = create_credit_card(client)
    Credit.objects.create(limite=1000.00, solde=0.00, carte_credit=card, client=client)


def create_credit_card(client):
    """ Initialise les paramètres nécessaire pour avoir une carte de crédit (16 chiffres, VISA) """

    expire = fake.credit_card_expire(start="now", end="+10y", date_format="%m/%y").split("/")
    expire_month = expire[0]
    expire_year = expire[1]
    security_code = fake.credit_card_security_code(card_type='visa16')
    card_number = fake.credit_card_number(card_type='visa16')

    card = CarteCredit.objects.create(nom_titulaire=client.full_name(), annee_expiration=expire_year,
                                      mois_expiration=expire_month, cvv=security_code, num_carte=card_number)
    return card
