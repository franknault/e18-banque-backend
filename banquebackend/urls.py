"""banquebackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from api.tasks import task_thread

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.client.urls')),
    path('api/', include('api.compte.urls')),
    path('api/', include('api.transaction.urls')),
    path('api/', include('api.transfert.urls')),
    path('api/', include('api.administrateur.urls'))
]

# TODO : Trouver une meilleure place pour appeler la méthode.
task_thread()
