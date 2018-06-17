import threading
import time
from django.utils import timezone
from datetime import timedelta
from django.conf import settings

from api.models import Transaction

def task_thread():
    """ Fonction permettant de démarrer un thread pour la vérification des transactions expirées """

    t = threading.Thread(target=check_trx, args=(), kwargs={})
    t.setDaemon(True)
    t.start()
    return True


def check_trx():
    """ Effectue la vérification et la modification des transactions expirées """
    while True:
        print("Clean up des transactions 'GEL'")
        # Vérifie les etats de transaction dans la base de données
        threshold = timezone.now() - timedelta(minutes=settings.TRANSACTION_EXPIRE)
        queryset = Transaction.objects.filter(date_debut__lt=threshold, etat=Transaction.GELE)
        if queryset:
            for entry in queryset:
                entry.date_fin = timezone.now()
                entry.etat = Transaction.REFUSE
                entry.save()

        time.sleep(settings.TRANSACTION_LOOKUP)
