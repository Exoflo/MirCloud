from django import forms
from.models import *
from django.core import validators

class Login(forms.Form):
    identifiant_secret = forms.CharField(max_length=16, required=True)
    botcatcher = forms.CharField(required = False, widget = forms.HiddenInput, validators=[validators.MaxLengthValidator(0)])


    

