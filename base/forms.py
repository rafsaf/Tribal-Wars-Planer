from bootstrap_datepicker_plus import DatePickerInput
from django import forms
from . import models


class New_Outline_Form(forms.Form):
    nazwa = forms.CharField(max_length=20, label='Nazwa Rozpiski', widget=forms.Textarea)
    data_akcji = forms.DateField(widget=DatePickerInput(format='%Y-%m-%d'), label='Data Akcji')
    swiat = forms.ChoiceField(choices=[], label='Świat')

class Wojsko_Outlines_Form(forms.ModelForm):
    class Meta:
        model = models.New_Outline
        fields = ['zbiorka_wojsko']
        labels = {
            'zbiorka_wojsko': 'Zbiórka Wojsko'
        }


class Obrona_Outlines_Form(forms.ModelForm):
    class Meta:
        model = models.New_Outline
        fields = ['zbiorka_obrona']
        labels = {
            'zbiorka_obrona': 'Zbiórka Obrona'
        }

class Moje_plemie_skrot_Form(forms.Form):
    plemie = forms.ChoiceField(choices=[], label='Moje plemię', required=False)


class Przeciwne_plemie_skrot_Form(forms.Form):
    plemie = forms.ChoiceField(choices=[], label='Przeciwne plemię', required=False)