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
    list_display = ('username', 'first_name', 'last_name', 'email', 'password', 'is_active',
                    'is_staff', 'is_superuser', 'last_login', 'date_joined')

admin.site.register(InfoAuthentification, CustomUserAdmin)