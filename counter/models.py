
from django import forms
Input1 = ['Pays', 'segment', 'Disponibilité','Motorisation','Transmission']

class counter(forms.Form):
    Pays = forms.ChoiceField(choices=[('', '')])
    segment = forms.ChoiceField(choices=[('', '')])
    Disponibilité = forms.ChoiceField(choices=[('', '')])
    Motorisation = forms.ChoiceField(choices=[('', '')])
    Transmission = forms.ChoiceField(choices=[('', '')])

   