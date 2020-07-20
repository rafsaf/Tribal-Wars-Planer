
from django import forms
from django.core.exceptions import MultipleObjectsReturned
from plemiona_pliki import basic_classes as basic
from . import models


class New_Outline_Form(forms.Form):
    nazwa = forms.CharField(
        max_length=20, label="Nazwa Rozpiski", widget=forms.Textarea
    )
    data_akcji = forms.DateField()
    swiat = forms.ChoiceField(choices=[], label="Świat")


# Dodac kiedys kwarg world-klasa Wolrd, by sprawdzić dokładnie czy wojsko i obrona poprawne
class Wojsko_Outline_Form(forms.ModelForm):
    class Meta:
        model = models.New_Outline
        fields = ["zbiorka_wojsko"]
        labels = {"zbiorka_wojsko": "Zbiórka Wojsko"}

    def clean_zbiorka_wojsko(self):
        text = self.cleaned_data["zbiorka_wojsko"]

        if text == "":
            pass
        else:
            new = ""
            for i, text_line in enumerate(text.split("\r\n")):

                if text_line == "":
                    continue
                line = text_line.split(",")
                if len(line) not in {12, 13, 14, 15, 16, 17}:
                    self.add_error(
                        "zbiorka_wojsko", "Błąd w lini {}: {}".format(i + 1, text_line)
                    )
                    return
                else:
                    for index, element in enumerate(line):
                        if index == 0:
                            try:
                                wioska = basic.Wioska(element)
                            except ValueError:
                                self.add_error(
                                    "zbiorka_wojsko",
                                    "Błąd w lini {}: {}".format(i + 1, text_line),
                                )
                                return
                        elif index != len(line) - 1:
                            if not element.isnumeric():
                                self.add_error(
                                    "zbiorka_wojsko",
                                    "Błąd w lini {}: {}".format(i + 1, text_line),
                                )
                                return
                        else:
                            if not element == "":
                                self.add_error(
                                    "zbiorka_wojsko",
                                    "Błąd w lini {}: {}".format(i + 1, text_line),
                                )
                                return

                if new == "":
                    new = text_line
                else:
                    new += "\r\n" + text_line
            return new
        return text


# Dodac kiedys kwarg world-klasa Wolrd, by sprawdzić dokładnie czy wojsko i obrona poprawne
class Obrona_Outline_Form(forms.ModelForm):
    class Meta:
        model = models.New_Outline
        fields = ["zbiorka_obrona"]
        labels = {"zbiorka_obrona": "Zbiórka Obrona"}

    def clean_zbiorka_obrona(self):
        text = self.cleaned_data["zbiorka_obrona"]

        if text == "":
            pass
        else:
            new = ""
            for i, text_line in enumerate(text.split("\r\n")):

                if text_line == "":
                    continue
                line = text_line.split(",")
                if len(line) not in {12, 13, 14, 15, 16, 17}:
                    self.add_error(
                        "zbiorka_obrona", "Błąd w lini {}: {}".format(i + 1, text_line)
                    )
                    return
                else:
                    for index, element in enumerate(line):
                        if index == 0:
                            try:
                                wioska = basic.Wioska(element)
                            except ValueError:
                                self.add_error(
                                    "zbiorka_obrona",
                                    "Błąd w lini {}: {}".format(i + 1, text_line),
                                )
                                return
                        elif index == 1:
                            if not element in {"w wiosce", "w drodze"}:
                                self.add_error(
                                    "zbiorka_obrona",
                                    "Błąd w lini {}: {}".format(i + 1, text_line),
                                )
                                return
                        elif index != len(line) - 1:
                            if not element.isnumeric():
                                self.add_error(
                                    "zbiorka_obrona",
                                    "Błąd w lini {}: {}".format(i + 1, text_line),
                                )
                                return
                        else:
                            if not element == "":
                                self.add_error(
                                    "zbiorka_obrona",
                                    "Błąd w lini {}: {}".format(i + 1, text_line),
                                )
                                return

                if new == "":
                    new = text_line
                else:
                    new += "\r\n" + text_line

            return new
        return text


class Moje_plemie_skrot_Form(forms.Form):
    plemie1 = forms.ChoiceField(choices=[], label="Moje plemię", required=False)

    def clean_plemie1(self):
        plemie = self.cleaned_data["plemie1"]
        if plemie == "banned":
            self.add_error("plemie1", "Wybierz plemię z listy")
            return
        return plemie


class Przeciwne_plemie_skrot_Form(forms.Form):
    plemie2 = forms.ChoiceField(choices=[], label="Przeciwne plemię", required=False)

    def clean_plemie2(self):
        plemie = self.cleaned_data["plemie2"]
        if plemie == "banned":
            self.add_error("plemie2", "Wybierz plemię z listy")
            return
        return plemie


class Get_Deff_Form(forms.Form):

    radius = forms.IntegerField(
        min_value=0,
        max_value=40,
        label="Promień",
        widget=forms.NumberInput,
        help_text="Np. Odległość między 500|500 a 500|503 to 3.",
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
        super(Get_Deff_Form, self).__init__(*args, **kwargs)

    def clean_ally_players(self):
        ally_players = self.cleaned_data["ally_players"].split()
        player_id = []
        for name in ally_players:
            try:
                player = models.Player.objects.get(name=name, world=self.world)
            except MultipleObjectsReturned as error:
                self.add_error(
                    "ally_players",
                    name
                    + ": "
                    + str(error)
                    + ", contact with admin"
                    + ", for now remove player and proceed",
                )
            except Exception:
                self.add_error("ally_players", "Nie istnieje gracz {}".format(name))
                return
            player_id.append(str(player.player_id))
        return ",".join(player_id)

    def clean_enemy_players(self):
        enemy_players = self.cleaned_data["enemy_players"].split()
        player_id = []
        for name in enemy_players:
            try:
                player = models.Player.objects.get(name=name, world=self.world)
            except MultipleObjectsReturned as error:
                self.add_error(
                    "enemy_players",
                    name
                    + ": "
                    + str(error)
                    + ", contact with admin"
                    + ", for now remove player and proceed",
                )
            except Exception:
                self.add_error("enemy_players", "Nie istnieje gracz {}".format(name))
                return
            player_id.append(str(player.player_id))
        return ",".join(player_id)

    def clean_excluded(self):
        try:
            village_list = basic.Wiele_wiosek(self.cleaned_data["excluded"])
        except ValueError as error:
            self.add_error("excluded", str(error))
            return
        return village_list


class Initial_Period_Outline_Player_Choose_Form(forms.Form):
    player = forms.ChoiceField(choices=[], label="Dodaj gracza", required=False)

    def clean_player(self):
        player = self.cleaned_data["player"]
        if player == "banned":
            player = ""
        return player


class Initial_Period_Outline_Player_Form(forms.Form):
    players = forms.CharField(
        max_length=1500,
        #hidden instead of text field change later
        widget=forms.HiddenInput,
        label="Gracze, którzy przejmują",
        required=False,
    )
    max_distance = forms.IntegerField(
        label="Max odległość od startu do celu - ilość kratek, domyślnie 50",
        required=False,
        widget=forms.NumberInput,
        initial=50,
    )
    target = forms.CharField(
        max_length=15000,
        widget=forms.Textarea,
        label="Cele",
        help_text="Kordy po spacji lub enterze",
        required=False,
    )

    def __init__(self, *args, **kwargs):
        self.world = kwargs.pop("world")
        super(Initial_Period_Outline_Player_Form, self).__init__(*args, **kwargs)

    def clean_players(self):
        players = self.cleaned_data["players"]
        if players == "":
            return players
        for name in players.split("\r\n"):
            try:
                players = models.Player.objects.get(name=name, world=self.world)
            except MultipleObjectsReturned as error:
                self.add_error(
                    "players",
                    name
                    + ": "
                    + str(error)
                    + ", contact with admin"
                    + ", for now remove player and proceed",
                )
                return
            except Exception:
                self.add_error("players", "Nie istnieje gracz {}".format(name))
                return
        return players

    def clean_target(self):
        try:
            village_list = basic.Wiele_wiosek(self.cleaned_data["target"])
        except ValueError as error:
            self.add_error("target", str(error))
            return
        for village in self.cleaned_data["target"].split():
            try:
                v = models.Village.objects.get(
                    x=village[0:3], y=village[4:7], world=self.world
                )
            except Exception:
                self.add_error(
                    "target",
                    "W bazie świata {} nie istnieje wioska {}".format(
                        self.world, village
                    ),
                )
                return
        return village_list

class Weight_form(forms.Form):
    start = forms.CharField(max_length=7, widget=forms.HiddenInput)
    distance = forms.FloatField(widget=forms.HiddenInput)
    order = forms.IntegerField(widget=forms.HiddenInput)
    off = forms.IntegerField(widget=forms.NumberInput)
    snob = forms.IntegerField(widget=forms.NumberInput)
    player = forms.CharField(max_length=20, widget=forms.HiddenInput)
