""" App forms """
from django.forms import BaseFormSet
from django import forms
from tribal_wars import basic
from . import models
from django.utils.translation import gettext_lazy


class OutlineForm(forms.Form):
    """ New Outline Form """

    name = forms.CharField(
        max_length=20,
        label=gettext_lazy("Outline Name"),
        widget=forms.Textarea,
    )
    date = forms.DateField(label=gettext_lazy("Date"))
    world = forms.ChoiceField(choices=[], label=gettext_lazy("World"))


class OffTroopsForm(forms.ModelForm):
    """ Pasted data from army script """

    class Meta:
        model = models.Outline
        fields = ["off_troops"]
        labels = {"off_troops": gettext_lazy("Army collection")}

    def __init__(self, *args, **kwargs):
        self.outline = kwargs.pop("outline")
        super(OffTroopsForm, self).__init__(*args, **kwargs)

    def clean_off_troops(self):
        """ User's input from script """
        text = self.cleaned_data["off_troops"].rstrip()
        if text == "":
            self.add_error(
                field=None, error=gettext_lazy("Text cannot be empty!")
            )
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
        labels = {"deff_troops": gettext_lazy("Deff collection")}

    def __init__(self, *args, **kwargs):
        self.outline = kwargs.pop("outline")
        super(DeffTroopsForm, self).__init__(*args, **kwargs)

    def clean_deff_troops(self):
        """ User's input from script """
        text = self.cleaned_data["deff_troops"].rstrip()
        if text == "":
            self.add_error(
                field=None, error=gettext_lazy("Text cannot be empty!")
            )
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

    plemie1 = forms.ChoiceField(
        choices=[], label=gettext_lazy("Ally tribe"), required=False
    )

    def clean_plemie1(self):
        """ User's tags input """
        plemie = self.cleaned_data["plemie1"]
        if plemie == "banned":
            self.add_error("plemie1", gettext_lazy("Select tribe from list"))
            return None
        return plemie


class EnemyTribeTagForm(forms.Form):
    """ Add enemy tribes to outline """

    plemie2 = forms.ChoiceField(
        choices=[], label=gettext_lazy("Enemy tribe"), required=False
    )

    def clean_plemie2(self):
        """ User's tag input """
        plemie = self.cleaned_data["plemie2"]
        if plemie == "banned":
            self.add_error("plemie2", gettext_lazy("Select tribe from list"))
            return None
        return plemie


class GetDeffForm(forms.Form):
    """ GetDeff function """

    radius = forms.IntegerField(
        min_value=0,
        max_value=100,
        label=gettext_lazy("Radius"),
        widget=forms.NumberInput,
        initial=30,
    )

    ally_players = forms.CharField(
        max_length=300,
        label=gettext_lazy("Other ally players"),
        help_text=gettext_lazy(
            "Exact nicknames separated by a space or an entry."
        ),
        required=False,
    )

    enemy_players = forms.CharField(
        max_length=300,
        label=gettext_lazy("Other enemy players"),
        help_text=gettext_lazy(
            "Exact nicknames separated by a space or an entry."
        ),
        required=False,
    )

    excluded = forms.CharField(
        max_length=300,
        label=gettext_lazy("Excluded enemy villages"),
        required=False,
        help_text=gettext_lazy(
            "Exact coords separated by a space or an entry."
        ),
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
                    self.add_error(
                        "ally_players",
                        gettext_lazy("There is no player: ") + str(name),
                    )
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
                    self.add_error(
                        "enemy_players",
                        gettext_lazy("There is no player: ") + str(name),
                    )
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


class InitialOutlineForm(forms.Form):
    """ New Initial Outline """

    target = forms.CharField(
        max_length=15000,
        widget=forms.Textarea,
        label=gettext_lazy("Targets"),
        required=False,
        initial="\r\n---"
    )
    # min_off = forms.IntegerField(
    #     widget=forms.NumberInput(),
    #     min_value=1,
    #     max_value=28000,
    #     label=gettext_lazy("Min. off units number"),
    #     initial=19000,
    # )
    # front_dist = forms.IntegerField(
    #     widget=forms.NumberInput(),
    #     min_value=0,
    #     max_value=40,
    #     label=gettext_lazy("Distance from front line"),
    #     initial=12,
    # )

    def __init__(self, *args, **kwargs):
        self.world = kwargs.pop("world")
        super(InitialOutlineForm, self).__init__(*args, **kwargs)
        # self.fields["min_off"].widget.attrs["class"] = "form-control"
        # self.fields["front_dist"].widget.attrs["class"] = "form-control"

    def clean_target(self):
        """ User's input Villages """
        basic_villages = []
        count_underline = 0

        data = self.cleaned_data["target"].rstrip().split("\r\n")
        for i, info in enumerate(data):
            info = info.split(":")
            if len(info) != 3:
                if info == ["---"]:
                    count_underline += 1
                    if count_underline > 1:
                        self.add_error("target", i)
                    continue
                else:
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
        if count_underline == 0:
            self.add_error("target", len(data) + 1)
        village_list = basic.many_villages(" ".join(basic_villages))
        villages_id = [
            f"{i.x_coord}{i.y_coord}{self.world}" for i in village_list
        ]
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

class AvailableTroopsForm(forms.ModelForm):
    class Meta:
        model = models.Outline
        fields = ["initial_outline_min_off", "initial_outline_front_dist",]
        labels = {
            "initial_outline_min_off": gettext_lazy("Min. off units number"),
            "initial_outline_front_dist": gettext_lazy("Distance from front line"),
        }

class SettingDateForm(forms.ModelForm):
    class Meta:
        model = models.Outline
        fields = ["date",]
        labels = {
            "date": gettext_lazy("Date"),
        }


class WeightForm(forms.Form):
    """ Change weight model """

    weight_id = forms.IntegerField(widget=forms.HiddenInput)
    off = forms.IntegerField(
        widget=forms.NumberInput, label=gettext_lazy("Off"), min_value=0
    )
    nobleman = forms.IntegerField(
        widget=forms.NumberInput, label=gettext_lazy("Noble"), min_value=0
    )


class PeriodForm(forms.ModelForm):
    """ One Period for OutlineTime """

    from_number = forms.IntegerField(
        min_value=0, label=gettext_lazy("From"), required=False
    )
    to_number = forms.IntegerField(
        min_value=0, label=gettext_lazy("To"), required=False
    )

    class Meta:
        model = models.PeriodModel
        exclude = ["outline_time", "from_number", "to_number"]
        labels = {
            "status": gettext_lazy("Mode"),
            "from_number": gettext_lazy("From"),
            "to_number": gettext_lazy("To"),
            "unit": gettext_lazy("Unit"),
            "from_time": gettext_lazy("Min. time"),
            "to_time": gettext_lazy("Max. time"),
        }

    def __init__(self, *args, **kwargs):
        super(PeriodForm, self).__init__(*args, **kwargs)
        self.fields["status"].widget.attrs["class"] = "form-control"
        self.fields["unit"].widget.attrs["class"] = "form-control"
        self.fields["from_number"].widget.attrs["class"] = "form-control"
        self.fields["to_number"].widget.attrs["class"] = "form-control"
        self.fields["from_time"].widget.attrs[
            "class"
        ] = "time-timepicker form-control"
        self.fields["to_time"].widget.attrs[
            "class"
        ] = "time-timepicker form-control"

    def clean(self):
        status = self.cleaned_data.get("status")
        time1 = self.cleaned_data.get("from_time")
        time2 = self.cleaned_data.get("to_time")
        number1 = self.cleaned_data.get("from_number")
        number2 = self.cleaned_data.get("to_number")
        if time2 < time1:
            self.add_error("from_time", "time2<time1")
        if status in {"random", None}:
            if number1 is None:
                self.add_error("from_number", "None")
            if number2 is None:
                self.add_error("to_number", "None")
            try:
                greater_is_smaller = bool(number2 < number1)
            except TypeError:
                pass
            else:
                if greater_is_smaller:
                    self.add_error("from_number", "time2<time1")
        if status == "all":
            if number1 is not None:
                self.add_error("from_number", "not None")
            if number2 is not None:
                self.add_error("to_number", "not None")
        if status == "exact":
            if number1 is not None:
                self.add_error("from_number", "not None")
            if number2 is None:
                self.add_error("to_number", "not None")


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
            status = form.cleaned_data.get("status")
            unit = form.cleaned_data.get("unit")
            time1 = form.cleaned_data.get("from_time")
            time2 = form.cleaned_data.get("to_time")
            number1 = form.cleaned_data.get("from_number")
            number2 = form.cleaned_data.get("to_number")
            if not any([status, unit, time1, time2, number1, number2]):
                continue
            if unit == "noble":
                if status == "all":
                    if not all_nobleman:
                        all_nobleman = True
                    else:
                        raise forms.ValidationError(
                            gettext_lazy(
                                "Mode All can be used only once per unit"
                            )
                        )
                from_time_nob.append((time1, status))
                to_time_nob.append((time2, status))
            elif unit == "ram":
                if status == "all":
                    if not all_ram:
                        all_ram = True
                    else:
                        raise forms.ValidationError(
                            gettext_lazy(
                                "Mode All can be used only once per unit"
                            )
                        )
                from_time_ram.append((time1, status))
                to_time_ram.append((time2, status))

        if not all_nobleman or not all_ram:
            raise forms.ValidationError(
                gettext_lazy(
                    "Mode All must be used at least once for noble and for off."
                )
            )

        from_time_nob.sort(key=lambda tup: tup[0])
        to_time_nob.sort(key=lambda tup: tup[0])
        from_time_ram.sort(key=lambda tup: tup[0])
        to_time_ram.sort(key=lambda tup: tup[0])

        if not from_time_nob[-1][1] == "all":
            raise forms.ValidationError(
                gettext_lazy(
                    "The All mode time frame MUST always be last for off and for noble."
                )
            )
        if not from_time_ram[-1][1] == "all":
            raise forms.ValidationError(
                gettext_lazy(
                    "The All mode time frame MUST always be last for off and for noble."
                )
            )

        nob_last = from_time_nob[-1][0]
        for n_from in to_time_nob:
            if nob_last < n_from[0] and n_from[1] != "all":
                raise forms.ValidationError(
                    gettext_lazy(
                        "The All mode cannot overlap with other time periods"
                    )
                )

        ram_last = from_time_ram[-1][0]
        for r_from in to_time_ram:
            if ram_last < r_from[0] and r_from[1] != "all":
                raise forms.ValidationError(
                    gettext_lazy(
                        "The All mode cannot overlap with other time periods"
                    )
                )


class ChooseOutlineTimeForm(forms.Form):
    choice = forms.ChoiceField(required=True, choices=[])

    def __init__(self, *args, **kwargs):
        super(ChooseOutlineTimeForm, self).__init__(*args, **kwargs)
        self.fields["choice"].widget.attrs["class"] = "form-control"


class CreateNewInitialTarget(forms.Form):
    target = forms.CharField(
        max_length=7,
        label=gettext_lazy("Target"),
        help_text=gettext_lazy("Valid coords, 7 chars"),
    )
    fake = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        self.outline = kwargs.pop("outline")
        super(CreateNewInitialTarget, self).__init__(*args, **kwargs)

    def clean_target(self):
        coord = self.cleaned_data["target"]
        x_coord = coord[0:3]
        y_coord = coord[4:7]
        village_id = x_coord + y_coord + str(self.outline.world)
        if models.TargetVertex.objects.filter(
            target=coord, outline=self.outline
        ).exists():
            self.add_error(
                "target", gettext_lazy("This village is already a target!")
            )
            return

        if not models.VillageModel.objects.filter(pk=village_id).exists():
            self.add_error(
                "target",
                gettext_lazy("Village with that coords did not found."),
            )
            return


class ChangeWeightMaxOff(forms.Form):
    off = forms.IntegerField(min_value=0)
    noble = forms.IntegerField(min_value=0)
