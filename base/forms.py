""" App forms """
from django.forms import BaseFormSet
from django import forms
from trbial_wars import basic
from . import models


class OutlineForm(forms.Form):
    """ New Outline Form """

    name = forms.CharField(max_length=20, label="Nazwa Rozpiski", widget=forms.Textarea)
    date = forms.DateField(label="Data Akcji")
    world = forms.ChoiceField(choices=[], label="Świat")


class OffTroopsForm(forms.ModelForm):
    """ Pasted data from army script """

    class Meta:
        model = models.Outline
        fields = ["off_troops"]
        labels = {"off_troops": "Zbiórka Wojsko"}

    def __init__(self, *args, **kwargs):
        self.outline = kwargs.pop("outline")
        super(OffTroopsForm, self).__init__(*args, **kwargs)

    def clean_off_troops(self):
        """ User's input from script """
        text = self.cleaned_data["off_troops"].rstrip()
        if text == "":
            self.add_error(field=None, error="Tekst nie może być pusty!")
            return None
        player_dictionary = basic.coord_to_player(self.outline)
        evidence = basic.world_evidence(self.outline.world)
        for i, text_line in enumerate(text.split("\r\n")):
            army = basic.Army(text_army=text_line, evidence=evidence)
            try:
                army.clean_init(player_dictionary)
            except basic.ArmyError:
                self.add_error("off_troops", i)
        return text


class DeffTroopsForm(forms.ModelForm):
    """ Pasted data from defence script """

    class Meta:
        model = models.Outline
        fields = {"deff_troops"}
        labels = {"deff_troops": "Zbiórka Obrona"}

    def __init__(self, *args, **kwargs):
        self.outline = kwargs.pop("outline")
        super(DeffTroopsForm, self).__init__(*args, **kwargs)

    def clean_deff_troops(self):
        """ User's input from script """
        text = self.cleaned_data["deff_troops"].rstrip()
        if text == "":
            self.add_error(field=None, error="Tekst nie może być pusty!")
            return None
        player_dictionary = basic.coord_to_player(self.outline)
        evidence = basic.world_evidence(self.outline.world)

        for i, text_line in enumerate(text.split("\r\n")):
            army = basic.Defence(text_army=text_line, evidence=evidence)
            try:
                army.clean_init(player_dictionary)
            except basic.DefenceError:
                self.add_error("deff_troops", i)

        return text


class MyTribeTagForm(forms.Form):
    """ Add ally tribes to outline """

    plemie1 = forms.ChoiceField(choices=[], label="Własne plemiona", required=False)

    def clean_plemie1(self):
        """ User's tags input """
        plemie = self.cleaned_data["plemie1"]
        if plemie == "banned":
            self.add_error("plemie1", "Wybierz plemię z listy")
            return None
        return plemie


class EnemyTribeTagForm(forms.Form):
    """ Add enemy tribes to outline """

    plemie2 = forms.ChoiceField(choices=[], label="Przeciwne plemiona", required=False)

    def clean_plemie2(self):
        """ User's tag input """
        plemie = self.cleaned_data["plemie2"]
        if plemie == "banned":
            self.add_error("plemie2", "Wybierz plemię z listy")
            return None
        return plemie


class GetDeffForm(forms.Form):
    """ GetDeff function """

    radius = forms.IntegerField(
        min_value=0,
        max_value=60,
        label="Promień",
        widget=forms.NumberInput,
        help_text="Np. Odległość między 500|500 a 500|503 to 3.",
        initial=30,
    )

    ally_players = forms.CharField(
        max_length=300,
        label="Dodaj współplemieńców spoza własnych plemion",
        help_text="Dokładne nicki oddzielone spacją lub enterem.",
        required=False,
    )

    enemy_players = forms.CharField(
        max_length=300,
        label="Dodaj przeciwników spoza przeciwnych plemion ",
        help_text="Dokładne nicki oddzielone spacją lub enterem.",
        required=False,
    )

    excluded = forms.CharField(
        max_length=300,
        label="Wykluczone wioski wroga",
        required=False,
        help_text="Podaj kordy wiosek oddzielając je spacją lub enterem.",
    )

    def __init__(self, *args, **kwargs):
        self.world = kwargs.pop("world")
        super(GetDeffForm, self).__init__(*args, **kwargs)

    def clean_ally_players(self):
        """ User's ally players input """
        ally_players = self.cleaned_data["ally_players"]
        ally_players_list = ally_players.strip().split()

        player_query = models.Player.objects.filter(
            name__in=ally_players_list, world=self.world
        )
        if len(ally_players_list) != player_query.count():
            name_set = set()
            for player in player_query:
                name_set.add(player.name)
            for name in ally_players_list:
                if name not in name_set:
                    self.add_error("ally_players", f"Nie istnieje gracz {name}")
                    return None
        return ally_players

    def clean_enemy_players(self):
        """ User's enemy players input  """
        enemy_players = self.cleaned_data["enemy_players"]
        enemy_players_list = self.cleaned_data["enemy_players"].strip().split()

        player_query = models.Player.objects.filter(
            name__in=enemy_players_list, world=self.world
        )
        if len(enemy_players_list) != player_query.count():
            name_set = set()
            for player in player_query:
                name_set.add(player.name)
            for name in enemy_players_list:
                if name not in name_set:
                    self.add_error("enemy_players", f"Nie istnieje gracz {name}")
                    return None
        return enemy_players

    def clean_excluded(self):
        """ Excluded Villages """
        villages = self.cleaned_data["excluded"]
        try:
            village_list = basic.many_villages(self.cleaned_data["excluded"])
        except basic.VillageError as error:
            self.add_error("excluded", str(error))
            return None
        return villages


class InitialFormTime(forms.Form):
    nob_enter = forms.TimeField(label="Minimalny czas wejścia grubych")
    nob_end = forms.TimeField(label="Maksymalny czas wejścia grubych")
    off_enter = forms.TimeField(label="Minimalny czas wejścia offów")
    off_end = forms.TimeField(label="Maksymalny czas wejścia offów")


class InitialOutlineForm(forms.Form):
    """ New Initial Outline """

    target = forms.CharField(
        max_length=15000,
        widget=forms.Textarea,
        label="Cele",
        help_text="Kordy po enterze",
        required=False,
    )

    def __init__(self, *args, **kwargs):
        self.world = kwargs.pop("world")
        super(InitialOutlineForm, self).__init__(*args, **kwargs)

    def clean_target(self):
        """ User's input Villages """
        basic_villages = []
        for i, info in enumerate(self.cleaned_data["target"].rstrip().split("\r\n")):
            info = info.split(":")
            if len(info) != 3:
                self.add_error("target", i)
                continue
            try:
                coord = info[0]
                village = basic.Village(coord)
            except basic.VillageError:
                self.add_error("target", i)
                continue
            if not info[1].isnumeric() or not info[2].isnumeric():
                self.add_error("target", i)
                continue
            basic_villages.append(village.coord)
        if len(self.errors) > 0:
            return None

        village_list = basic.many_villages(" ".join(basic_villages))
        villages_id = [f"{i.x_coord}{i.y_coord}{self.world}" for i in village_list]
        village_models = models.VillageModel.objects.filter(id__in=villages_id)
        if len(village_list) != village_models.count():
            village_set = [
                f"{village_model.x_coord}|{village_model.y_coord}"
                for village_model in village_models
            ]
            for i, village in enumerate(village_list):
                if village.coord not in village_set:
                    self.add_error("target", i)
                    return None
        return self.cleaned_data["target"]


class WeightForm(forms.Form):
    """ Change weight model """
    weight_id = forms.IntegerField(widget=forms.HiddenInput)
    off = forms.IntegerField(widget=forms.NumberInput, min_value=0)
    nobleman = forms.IntegerField(widget=forms.NumberInput, label='Szlachcic', min_value=0)


class PeriodForm(forms.ModelForm):
    """ One Period for OutlineTime """
    from_number = forms.IntegerField(min_value=0, label='Od', required=False)
    to_number = forms.IntegerField(min_value=0, label='Do', required=False)
    class Meta:
        model = models.PeriodModel
        exclude = ['outline_time', 'from_number', 'to_number']
        labels = {
            'status': 'Tryb',
            'from_number': 'Od',
            'to_number': 'Do',
            'unit': 'Jednostka',
            'from_time': 'Min. czas',
            'to_time': 'Max. czas',
        }

    def __init__(self, *args, **kwargs):
        super(PeriodForm, self).__init__(*args, **kwargs)
        self.fields['status'].widget.attrs['class'] = 'form-control'
        self.fields['unit'].widget.attrs['class'] = 'form-control'
        self.fields['from_time'].widget.attrs['class'] = 'time-timepicker form-control'
        self.fields['to_time'].widget.attrs['class'] = 'time-timepicker form-control'
        self.fields['from_number'].widget.attrs['class'] = 'form-control'
        self.fields['to_number'].widget.attrs['class'] = 'form-control'

    def clean(self):
        status = self.cleaned_data.get('status')
        time1 = self.cleaned_data.get('from_time')
        time2 = self.cleaned_data.get('to_time')
        number1 = self.cleaned_data.get('from_number')
        number2 = self.cleaned_data.get('to_number')
        if time2 < time1:
            self.add_error('from_time', 'time2<time1')
        if status in {'Losowo', None}:
            if number1 is None:
                self.add_error('from_number', 'None')
            if number2 is None:
                self.add_error('to_number', 'None')
            try:
                greater_is_smaller = bool(number2 < number1)
            except TypeError:
                pass
            else:
                if greater_is_smaller:
                    self.add_error('from_number', 'time2<time1')
        if status == 'Wszystkie':
            if number1 is not None:
                self.add_error('from_number', 'not None')
            if number2 is not None:
                self.add_error('to_number', 'not None')
        if status == 'Dokładnie':
            if number1 is not None:
                self.add_error('from_number', 'not None')
            if number2 is None:
                self.add_error('to_number', 'not None')

class BasePeriodFormSet(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return

        from_time_nob = []
        from_time_ram = []
        to_time_nob = []
        to_time_ram = []
        all_nobleman = False
        all_ram = False

        for form in self.forms:
            status = form.cleaned_data.get('status')
            unit = form.cleaned_data.get('unit')
            time1 = form.cleaned_data.get('from_time')
            time2 = form.cleaned_data.get('to_time')
            number1 = form.cleaned_data.get('from_number')
            number2 = form.cleaned_data.get('to_number')
            if not any([status, unit, time1, time2, number1, number2]):
                continue
            if unit == 'Szlachcic':
                if status == 'Wszystkie':
                    if not all_nobleman:
                        all_nobleman = True
                    else:
                        raise forms.ValidationError('Tryb Wszystkie może być użyty tylko raz dla każdej jednostki.')
                from_time_nob.append((time1, status))
                to_time_nob.append((time2, status))
            elif unit == 'Taran':
                if status == 'Wszystkie':
                    if not all_ram:
                        all_ram = True
                    else:
                        raise forms.ValidationError('Tryb Wszystkie może być użyty tylko raz dla każdej jednostki.')                      
                from_time_ram.append((time1, status))
                to_time_ram.append((time2, status))
            else:
                raise forms.ValidationError('???!')

        if not all_nobleman or not all_ram:
            raise forms.ValidationError('Tryb Wszystkie musi zostać użyty co najmniej raz dla szlachty oraz dla offów.')

        from_time_nob.sort(key=lambda tup: tup[0])
        to_time_nob.sort(key=lambda tup: tup[0])
        from_time_ram.sort(key=lambda tup: tup[0])
        to_time_ram.sort(key=lambda tup: tup[0])
        
        if not from_time_nob[-1][1] == 'Wszystkie':
            raise forms.ValidationError('Przedział czasowy trybu Wszystkie MUSI być zawsze ostatni dla offów oraz dla szlachciców.')
        if not from_time_ram[-1][1] == 'Wszystkie':
            raise forms.ValidationError('Przedział czasowy trybu Wszystkie MUSI być zawsze ostatni dla offów oraz dla szlachciców.')

        nob_last = from_time_nob[-1][0]
        for n_from in to_time_nob:
            if nob_last < n_from[0] and n_from[1] != 'Wszystkie':
                raise forms.ValidationError('Tryb Wszystkie nie może pokrywać się z innymi przedziałami czasowymi.')

        ram_last = from_time_ram[-1][0]
        for r_from in to_time_ram:
            if ram_last < r_from[0] and r_from[1] != 'Wszystkie':
                raise forms.ValidationError('Tryb Wszystkie nie może pokrywać się z innymi przedziałami czasowymi.')

class ChooseOutlineTimeForm(forms.Form):
    choice = forms.ChoiceField(required=True, choices=[])
    def __init__(self, *args, **kwargs):
        super(ChooseOutlineTimeForm, self).__init__(*args, **kwargs)
        self.fields['choice'].widget.attrs['class'] = 'form-control'