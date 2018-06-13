from django.db.models.signals import post_save
from django.dispatch import receiver
from api.models import *
from decimal import Decimal

from faker import Faker

fake = Faker()


@receiver(post_save, sender=Transaction)
def gel_fond(sender, instance, **kwargs):
    if instance.etat == Transaction.GELE:
        compte = instance.compte
        compte.solde = Decimal(compte.solde) + Decimal(instance.montant)
        compte.save()

    if instance.etat == Transaction.ACCEPTE:
        compte.save()

    if instance.etat == Transaction.REFUSE:
        compte = instance.compte
        compte.solde = Decimal(compte.solde) + Decimal(instance.montant)
        compte.save()


@receiver(post_save, sender=Courant)
def update_num_compte_courant(sender, instance, **kwargs):
    prefix = 'NRB'
    num = prefix + format(instance.id, '05')
    Compte.objects.filter(id=instance.id).update(num_compte=num)


@receiver(post_save, sender=Credit)
def update_num_compte_credit(sender, instance, **kwargs):
    prefix = 'NRB'
    num = prefix + format(instance.id, '05')
    Compte.objects.filter(id=instance.id).update(num_compte=num)


@receiver(post_save, sender=Client)
def generate_compte(sender, instance, **kwargs):
    client = Client.objects.get(id=instance.id)
    create_courant(client)
    create_credit(client)


def create_courant(client):
    Courant.objects.create(solde=0.00, client=client)


def create_credit(client):
    card = create_credit_card(client)
    Credit.objects.create(limite=1000.00, solde=0.00, carte_credit=card, client=client)


def create_credit_card(client):
    expire = fake.credit_card_expire(start="now", end="+10y", date_format="%m/%y").split("/")
    expire_month = expire[0]
    expire_year = expire[1]
    security_code = fake.credit_card_security_code(card_type=None)
    card_number = fake.credit_card_number(card_type=None)

    card = CarteCredit.objects.create(nom_titulaire=client.full_name, annee_expiration=expire_year,
                                      mois_expiration=expire_month, cvv=security_code, num_carte=card_number)

    return card

