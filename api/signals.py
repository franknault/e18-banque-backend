from django.db.models.signals import post_save
from django.dispatch import receiver
from api.models import Compte


@receiver(post_save, sender=Compte)
def update_num_compte(sender, instance, **kwargs):
    prefix = 'NRB'
    num = prefix + format(instance.pk_compte, '05')
    Compte.objects.filter(pk_compte=instance.pk_compte).update(num_compte=num)