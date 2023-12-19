from django import forms
from .models import Games
from django.forms import fields


class GamesForm(forms.ModelForm):
    class Meta:
        model = Games
        fields = "__all__"


class UploadFileForm(forms.Form):
    file = forms.FileField(required=False, widget=forms.FileInput(attrs={'class': 'form-control', 'placeholder':
        'Upload "products.csv"', 'help_text': 'Choose a .csv file with products to enter'}))
