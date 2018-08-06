from django.conf.urls import url
from django.urls import include, path
from . import views

urlpatterns = [
    path('client', views.ClientProfile.as_view()),
    path('client/email', views.ClientEmail.as_view()),
    path('client/compte', views.ClientCompte.as_view()),
    path('client/compte/credit', views.ClientCompteCredit.as_view()),
    path('client/compte/courant', views.ClientCompteCourant.as_view()),
    path('client/adresse', views.ClientAdresse.as_view()),
    path('rest-auth/', include('rest_auth.urls')),
    path('admin/client', views.ClientsApi.as_view()),
    path('admin/client/<int:pk>', views.ClientId.as_view()),
    path('admin/client/<username>', views.ClientIdEmail.as_view()),
    path('admin/client/<int:pk>/adresse', views.ClientIdAdresses.as_view()),
    path('admin/client/<int:pk>/compte', views.ClientIdCompte.as_view()),
    path('admin/client/<int:pk>/compte/<int:pk_compte>', views.ClientIdCompteId.as_view()),
    path('admin/client/search?param=x', views.ClientSearch.as_view()),
]