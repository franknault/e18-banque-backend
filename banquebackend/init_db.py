from api.models import *
from datetime import date


def import_db():
    # Info Client
    info_roni = InfoAuthentification.objects.create(username="roni", password="gti525", email="roni@gmail.com")
    info_fodil = InfoAuthentification.objects.create(username="fodil", password="gti525", email="fodil@gmail.com")
    info_philippe = InfoAuthentification.objects.create(username="philippe", password="gti525", email="philippe@gmail.com")
    info_francis = InfoAuthentification.objects.create(username="francis", password="gti525", email="francis@gmail.com")
    info_javier = InfoAuthentification.objects.create(username="javier", password="gti525", email="javier@gmail.com")

    # Info Entreprise
    info_ubisoft = InfoAuthentification.objects.create(username="ubisoft", password="gti525", email="ubisoft@gmail.com")
    info_metro = InfoAuthentification.objects.create(username="metro", password="gti525", email="metro@gmail.com")

    # Admin
    info_admin = InfoAuthentification.objects.create(username="admin", password="admin", email="admin@gmail.com")
    info_root = InfoAuthentification.objects.create(username="root", password="root", email="root@gmail.com")

    # Client Particulier
    roni = Client.objects.create(nom_particulier="Moufarrej", prenom_particulier="Roni", sexe=Client.HOMME, type=Client.PARTICULIER,
                                 telephone="4504325678", date_naissance=date(1995,2,23), info_authentification=info_roni)
    fodil = Client.objects.create(nom_particulier="Benarbia", prenom_particulier="Fodil", sexe=Client.HOMME, type=Client.PARTICULIER,
                                  telephone="4509651234", date_naissance=date(2000,4,12), info_authentification=info_fodil)
    javier = Client.objects.create(nom_particulier="Beltran", prenom_particulier="Javier", sexe=Client.HOMME, type=Client.PARTICULIER,
                                   telephone="5149456543", date_naissance=date(1990,5,15), info_authentification=info_javier)
    philippe = Client.objects.create(nom_particulier="Godbout", prenom_particulier="Philippe", sexe=Client.HOMME, type=Client.PARTICULIER,
                                     telephone="4501236570", date_naissance=date(1987,12,12), info_authentification=info_philippe)
    francis = Client.objects.create(nom_particulier="Nault", prenom_particulier="Francis", sexe=Client.HOMME, type=Client.PARTICULIER,
                                    telephone="5609001232", date_naissance=date(1995,2,8), info_authentification=info_francis)
    Administrateur.objects.create(info_authentification=info_admin)
    Administrateur.objects.create(info_authentification=info_root)

    # Client Entreprise
    ubisoft = Client.objects.create(nom_entreprise="Ubisoft", numero_entreprise="54321", type=Client.ENTREPRISE,
                                    telephone="18009456780", info_authentification=info_ubisoft)
    metro = Client.objects.create(nom_entreprise="Metro", numero_entreprise="12345", type=Client.ENTREPRISE,
                                  telephone="18887432245", info_authentification=info_metro)

    # Adresses
    Adresse.objects.create(no_civique="43-6817", nom_rue="Av Montreal", code_postal="H1T2R9", ville="Montréal", pays="",
                           client=roni)
    Adresse.objects.create(no_civique="251", nom_rue="Rue St Denis", code_postal="H2R2E7", ville="Montréal",
                           pays="Canada", client=fodil)
    Adresse.objects.create(no_civique="7766", nom_rue="Av Percival", code_postal="H4X1T8", ville="Terrebonne",
                           pays="Canada", client=javier)
    Adresse.objects.create(no_civique="11727", nom_rue="George Street", code_postal="H8P1E1", ville="Lasalle",
                           pays="Canada", client=philippe)
    Adresse.objects.create(no_civique="17-5745", nom_rue="Rue Notre Dame E", code_postal="H1B2X8", ville="Montréal",
                           pays="Canada", client=francis)
    Adresse.objects.create(no_civique="3708", nom_rue="Av Montreal", code_postal="H1X2R7", ville="Montréal",
                           pays="Canada", client=ubisoft)
    Adresse.objects.create(no_civique="800", nom_rue="Rue St Hubert", code_postal="H2L4A2", ville="Montréal",
                           pays="Canada", client=metro)

    # Type Transaction
    vmt = TypeTransaction.objects.create(type="VMT", description="Virement d'un compte débit vers un compte débit.")
    pmt = TypeTransaction.objects.create(type="PMT", description="Paiement d'un compte débit vers un compte crédit.")
    act = TypeTransaction.objects.create(type="ACT", description="Achat d'un compte crédit vers un compte débit.")
    rbt = TypeTransaction.objects.create(type="RBT", description="Remboursement d'un compte crédit vers un compte crédit.")


def flush_db():
    Adresse.objects.all().delete()
    TypeTransaction.objects.all().delete()
    Client.objects.all().delete()
    Administrateur.objects.all().delete()
    InfoAuthentification.objects.all().delete()
    CarteCredit.objects.all().delete()
    Credit.objects.all().delete()
    Courant.objects.all().delete()
    Compte.objects.all().delete()

