""" App forms """

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

    start = forms.CharField(max_length=7, widget=forms.HiddenInput)
    distance = forms.FloatField(widget=forms.HiddenInput)
    order = forms.IntegerField(widget=forms.HiddenInput)
    off = forms.IntegerField(widget=forms.NumberInput)
    nobleman = forms.IntegerField(widget=forms.NumberInput)
    player = forms.CharField(max_length=20, widget=forms.HiddenInput)
