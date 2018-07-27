from django.urls import path
from . import views

urlpatterns = [
    path('client/transaction', views.TransactionCompte.as_view()),
    path('admin/transaction', views.TransactionsList.as_view()),
    path('admin/transaction/<int:pk>', views.TransactionId.as_view())
]
