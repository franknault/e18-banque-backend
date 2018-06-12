from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import InfoAuthentification

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = InfoAuthentification
        fields = ('__all__')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = InfoAuthentification
        fields = UserChangeForm.Meta.fields