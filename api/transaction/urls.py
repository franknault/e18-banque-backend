from django.urls import path
from . import views

urlpatterns = [
    path('transaction', views.TransactionsList.as_view()),
    path('transaction/<int:pk>', views.TransactionId.as_view())
]
