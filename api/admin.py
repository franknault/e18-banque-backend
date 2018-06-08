# Register your models here.
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import InfoAuthentification

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = InfoAuthentification
    list_display = ['username', 'password', 'nom_usager', 'mdp', 'courriel']

admin.site.register(InfoAuthentification, CustomUserAdmin)