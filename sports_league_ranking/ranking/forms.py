from django import forms
from .models import Games, Team
from django.forms import fields


class GamesForm(forms.ModelForm):
    team_1 = forms.CharField(label='team 1', max_length=100,
                             widget=forms.TextInput(attrs={'class': "form-control"}))
    team_2 = forms.CharField(label='team 2', max_length=100,
                             widget=forms.TextInput(attrs={'class': "form-control"}))
    class Meta:
        model = Games
        fields = "__all__"
        widgets = {
                   'team_1_score': forms.NumberInput(attrs={'class': 'form-control'}),
                   'team_2_score': forms.NumberInput(attrs={'class': 'form-control'}),
                   }

    def clean(self):
        cleaned_data =  super().clean()
        team1_name = self.cleaned_data.get('team_1')
        team_1, created = Team.objects.get_or_create(name=team1_name)
        self.cleaned_data.update({'team_1': team_1})
        team2_name = self.cleaned_data.get('team_2')
        team_2, created = Team.objects.get_or_create(name=team2_name)
        self.cleaned_data.update({'team_2': team_2})


class UploadFileForm(forms.Form):
    file = forms.FileField(
        required=True,
        widget=forms.FileInput(attrs={'class': 'form-control',
                                      'placeholder': 'Upload "products.csv"',
                                      'help_text': 'Choose a .csv file with products to enter'}))

