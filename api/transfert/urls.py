from django.urls import path

from . import views


urlpatterns = [
    path('transfert/virement', views.TransfertVirement.as_view()),
    path('transfert/paiement', views.TransfertPaiement.as_view()),
    path('transfert/achat', views.TransfertAchat.as_view()),
    path('transfert/remboursement', views.TransfertRemboursement.as_view()),
    path('transfert/<int:pk>', views.TransfertState.as_view())
]
