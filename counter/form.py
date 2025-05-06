from django import forms
import pandas as pd

#df = pd.read_excel('POWERTRAIN1.xlsx')
df = pd.DataFrame()
df1 = pd.read_excel('DONNEES_POWERTRAIN_FRANCE.xlsx')
df2 = pd.read_excel('EV_DATA_BASE_AC_042025.xlsx')
df = pd.concat([df1,df2])

class SearchForm(forms.Form):
    query_p = forms.ChoiceField(label='Pays', required=False)
    query_s = forms.ChoiceField(label='Segment', required=False)
    query_e = forms.ChoiceField(label='Disponibilité', required=False)
    query_i = forms.ChoiceField(label='Motorisation', required=False)
    query_j = forms.ChoiceField(label='Transmission',required=False)

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        # Récupérer les valeurs uniques des colonnes spécifiques de votre DataFrame et les utiliser pour remplir les options des listes déroulantes
        unique_values_p = df['Pays'].unique()
        unique_values_s = df['Segment'].unique()
        unique_values_e = df['Disponibilité'].unique()
        unique_values_i = df['Motorisation'].unique()
        unique_values_j = df['Transmission'].unique()

        # Ajouter les options des listes déroulantes avec les valeurs uniques des colonnes
        self.fields['query_p'].choices = [('', '---------')] + [(value, value) for value in unique_values_p]
        self.fields['query_s'].choices = [('', '---------')] + [(value, value) for value in unique_values_s]
        self.fields['query_e'].choices = [('', '---------')] + [(value, value) for value in unique_values_e]
        self.fields['query_i'].choices = [('', '---------')] + [(value, value) for value in unique_values_i]
        self.fields['query_j'].choices = [('', '---------')] + [(value, value) for value in unique_values_j]

    