from bootstrap_datepicker_plus import DatePickerInput
from django import forms
from . import models


class New_Outlines_Form(forms.ModelForm):
    class Meta:
        model = models.New_Outline
        fields = ['nazwa', 'data_akcji', 'swiat']
        widgets = {
            'data_akcji': DatePickerInput(),
            'swiat': forms.Select(choices=[("{}".format(i.world), "{}".format(i.world)) for i in models.World.objects.all()])
        }
        labels = {
            'nazwa': "Nazwa Rozpiski",
            'data_akcji': 'Data Akcji',

        }


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
    plemie = forms.ChoiceField(choices=[], label='Moje plemię')


class Przeciwne_plemie_skrot_Form(forms.Form):
    plemie = forms.ChoiceField(choices=[], label='Przeciwne plemię')