from django.db.models.signals import post_save
from django.dispatch import receiver
from api.models import *

from faker import Faker

fake = Faker()

@receiver(post_save, sender=Courant)
def update_num_compte_courant(sender, instance, **kwargs):
    prefix = 'NRB'
    num = prefix + format(instance.pk_compte, '05')
    Compte.objects.filter(pk_compte=instance.pk_compte).update(num_compte=num)


@receiver(post_save, sender=Credit)
def update_num_compte_credit(sender, instance, **kwargs):
    prefix = 'NRB'
    num = prefix + format(instance.pk_compte, '05')
    Compte.objects.filter(pk_compte=instance.pk_compte).update(num_compte=num)


@receiver(post_save, sender=Client)
def generate_compte(sender, instance, **kwargs):
    client = Client.objects.get(pk_client=instance.pk)
    create_courant(client)
    create_credit(client)


def create_courant(client):
    Courant.objects.create(solde=0.00, fk_client_id=client.pk)


def create_credit(client):
    pk_card = create_credit_card(client)
    Credit.objects.create(limite=1000.00, solde=0.00, fk_carte_credit_id=pk_card, fk_client_id=client.pk)


def create_credit_card(client):
    expire = fake.credit_card_expire(start="now", end="+10y", date_format="%m/%y").split("/")
    expire_month = expire[0]
    expire_year = expire[1]
    security_code = fake.credit_card_security_code(card_type=None)
    card_number = fake.credit_card_number(card_type=None)

    card = CarteCredit.objects.create(nom_titulaire=client.full_name, annee_expiration=expire_year,
                                      mois_expiration=expire_month, cvv=security_code, num_carte=card_number)

    return card.pk

