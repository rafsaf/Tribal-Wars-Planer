""" App forms """
from django.forms import BaseFormSet
from django import forms
from tribal_wars import basic, database_update
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
            self.add_error(field=None, error=gettext_lazy("Text cannot be empty!"))
            return None

        player_dictionary = basic.coord_to_player(self.outline)
        evidence = basic.world_evidence(self.outline.world)

        already_used_villages = set()

        for i, text_line in enumerate(text.split("\r\n")):
            army = basic.Army(text_army=text_line, evidence=evidence)
            if army.coord in already_used_villages:
                self.add_error("off_troops", i)
                continue
            else:
                already_used_villages.add(army.coord)

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
            self.add_error(field=None, error=gettext_lazy("Text cannot be empty!"))
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
        max_value=45,
        label=gettext_lazy("Radius"),
        widget=forms.NumberInput,
        help_text=gettext_lazy("Greater than or equal to 0 and less than or equal to 45."),
        initial=10,
    )

    excluded = forms.CharField(
        max_length=3000,
        widget=forms.Textarea,
        label=gettext_lazy("Excluded enemy secluded villages"),
        required=False,
        help_text=gettext_lazy("Exact coords separated by a space or an entry."),
    )

    def __init__(self, *args, **kwargs):
        self.world = kwargs.pop("world")
        super(GetDeffForm, self).__init__(*args, **kwargs)

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
        max_length=50000,
        widget=forms.Textarea,
        label=gettext_lazy("Targets"),
        required=False,
        strip=False
    )

    def __init__(self, *args, **kwargs):
        self.outline: models.Outline = kwargs.pop("outline")
        self.target_mode: basic.TargetMode = kwargs.pop("target_mode")
        super(InitialOutlineForm, self).__init__(*args, **kwargs)

    def clean_target(self):
        """ User's input Targets """
        
        data = self.cleaned_data["target"]
        data_lines = basic.TargetsData(data=data, world=self.outline.world)
        if data == "":
            data_lines.new_validated_data = ""
        else:
            data_lines.validate()

        if len(data_lines.errors_ids) == 0:
            if self.target_mode.is_real:
                self.outline.initial_outline_targets = data_lines.new_validated_data.strip()
            elif self.target_mode.is_fake:
                self.outline.initial_outline_fakes = data_lines.new_validated_data.strip()
            else:
                self.outline.initial_outline_ruins = data_lines.new_validated_data.strip()
            self.outline.save()

        for error_id in data_lines.errors_ids:
            self.add_error("target", error_id)
        return data


class AvailableTroopsForm(forms.ModelForm):
    class Meta:
        model = models.Outline
        fields = [
            "initial_outline_min_off",
            "initial_outline_front_dist",
            "initial_outline_excluded_coords",
            "initial_outline_target_dist",
        ]
        labels = {
            "initial_outline_min_off": gettext_lazy("Min. off units number"),
            "initial_outline_front_dist": gettext_lazy("Distance from front line"),
            "initial_outline_target_dist": gettext_lazy("Max Distance for nobles"),
        }
        help_texts = {
            "initial_outline_min_off": gettext_lazy(
                "Greater than or equal to 1 and less than or equal to 28000."
            ),
            "initial_outline_front_dist": gettext_lazy(
                "Greater than or equal to 0 and less than or equal to 45."
            ),
            "initial_outline_target_dist": gettext_lazy(
                "Greater than or equal to 0 and less than or equal to 150."
            ),
        }

    initial_outline_excluded_coords = forms.CharField(
        label=gettext_lazy("Excluded enemy villages coords (secluded villages)"),
        required=False,
        max_length=100000,
        help_text=gettext_lazy("Exact coords separated by a space or an entry"),
        widget=forms.Textarea,
    )

    def clean_initial_outline_excluded_coords(self):
        """ Excluded Villages """
        coords = self.cleaned_data["initial_outline_excluded_coords"]
        try:
            village_list = basic.many_villages(coords)
        except basic.VillageError as error:
            self.add_error("initial_outline_excluded_coords", str(error))


class SettingMessageForm(forms.ModelForm):
    class Meta:
        model = models.Outline
        fields = [
            "default_show_hidden",
            "title_message",
            "text_message",
        ]
        labels = {
            "default_show_hidden": gettext_lazy("Show all hidden"),
            "title_message": gettext_lazy("Title of message:"),
            "text_message": gettext_lazy("Content of message:"),
        }
        help_texts = {
            "title_message": gettext_lazy("Maximum length: 50"),
            "text_message": gettext_lazy("Maximum length: 500"),
        }
        widgets = {
            "text_message": forms.Textarea,
        }

    def clean_text_message(self):
        text = self.cleaned_data.get("text_message")
        length = len(text.replace("\r\n", "%0A"))
        if length > 500:
            raise forms.ValidationError(
                gettext_lazy("Ensure this value has at most 500 characters (it has ")
                + f" {length})."
            )


class SettingDateForm(forms.ModelForm):
    class Meta:
        model = models.Outline
        fields = [
            "date",
        ]
        labels = {
            "date": gettext_lazy("Set new date"),
        }


class SetNewOutlineFilters(forms.ModelForm):
    class Meta:
        model = models.Outline
        fields = [
            "filter_weights_min",
            "filter_weights_max",
            "filter_card_number",
            "filter_hide_front",
        ]

    def __init__(self, *args, **kwargs):
        super(SetNewOutlineFilters, self).__init__(*args, **kwargs)
        self.fields["filter_weights_min"].widget.attrs["class"] = "form-control"
        self.fields["filter_weights_max"].widget.attrs["class"] = "form-control"
        self.fields["filter_card_number"].widget.attrs["class"] = "form-control"
        self.fields["filter_hide_front"].widget.attrs["class"] = "form-control"

class SetTargetsMenuFilters(forms.ModelForm):
    class Meta:
        model = models.Outline
        fields = [
            "filter_targets_number",
        ]

    def __init__(self, *args, **kwargs):
        super(SetTargetsMenuFilters, self).__init__(*args, **kwargs)
        self.fields["filter_targets_number"].widget.attrs["class"] = "form-control"


class ModeOutlineForm(forms.ModelForm):
    class Meta:
        model = models.Outline
        fields = [
            "mode_off",
            "mode_noble",
            "mode_division",
            "mode_guide",
            "mode_split",
            "initial_outline_fake_limit",
            "initial_outline_catapult_default",
            "initial_outline_off_left_catapult",
        ]
        labels = {
            "mode_off": gettext_lazy("Choose the distance of the written offs:"),
            "mode_noble": gettext_lazy("Choose the distance of the written nobles:"),
            "mode_division": gettext_lazy("Choose how to split offs with nobles:"),
            "mode_guide": gettext_lazy(
                "Choose prefered way of writing required nobles:"
            ),
            "mode_split": gettext_lazy(
                "Choose how noble commands should be written out:"
            ),
            "initial_outline_fake_limit": gettext_lazy(
                "Maximum number of fakes from one off village:"
            ),
            "initial_outline_catapult_default": gettext_lazy(
                "Number of catapults in one ruin attack:"
            ),
            "initial_outline_off_left_catapult": gettext_lazy(
                "Number of catapults that will always be left in full offs:"
            ),
        }
        widgets = {
            "mode_off": forms.RadioSelect,
            "mode_noble": forms.RadioSelect,
            "mode_division": forms.RadioSelect,
            "mode_split": forms.RadioSelect,
            "mode_guide": forms.RadioSelect,
        }


#    def __init__(self, *args, **kwargs):
#        super(ModeOutlineForm, self).__init__(*args, **kwargs)
#        self.fields["mode_off"].widget.attrs["class"] = "form-check"
#        self.fields["mode_noble"].widget.attrs["class"] = "form-check"
#        self.fields["mode_division"].widget.attrs["class"] = "form-check"


class ModeTargetSetForm(forms.ModelForm):
    class Meta:
        model = models.TargetVertex
        fields = [
            "mode_off",
            "mode_noble",
            "mode_division",
            "mode_guide",
        ]
        widgets = {
            "mode_off": forms.RadioSelect,
            "mode_noble": forms.RadioSelect,
            "mode_division": forms.RadioSelect,
            "mode_guide": forms.RadioSelect,
        }
        labels = {
            "mode_off": "",
            "mode_noble": "",
            "mode_division": "",
            "mode_guide": "",
        }

class NightBonusSetForm(forms.Form):
    night_bonus = forms.BooleanField(
        required=False,
        label=gettext_lazy("Choose whether to avoid the night bonus"),
        initial=False,
    )
    enter_t1 = forms.IntegerField(
        min_value=0,
        max_value=24,
        label=gettext_lazy("Approximate hours of entry"),
        widget=forms.NumberInput,
        initial=7,
    )
    enter_t2 = forms.IntegerField(
        min_value=0,
        max_value=24,
        label=gettext_lazy("Approximate hours of the last entry"),
        widget=forms.NumberInput,
        initial=12,
    )
    def clean(self):
        super().clean()
        t1 = self.cleaned_data.get("enter_t1")
        t2 = self.cleaned_data.get("enter_t2")
        if t1 and t2:
            if t1 > t2:
                self.add_error("enter_t1", gettext_lazy("First value must be less or equal to second!"))


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
        self.fields["from_time"].widget.attrs["class"] = "time-timepicker form-control"
        self.fields["to_time"].widget.attrs["class"] = "time-timepicker form-control"

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
                            gettext_lazy("Mode All can be used only once per unit")
                        )
                from_time_nob.append((time1, status))
                to_time_nob.append((time2, status))
            elif unit == "ram":
                if status == "all":
                    if not all_ram:
                        all_ram = True
                    else:
                        raise forms.ValidationError(
                            gettext_lazy("Mode All can be used only once per unit")
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
                    gettext_lazy("The All mode cannot overlap with other time periods")
                )

        ram_last = from_time_ram[-1][0]
        for r_from in to_time_ram:
            if ram_last < r_from[0] and r_from[1] != "all":
                raise forms.ValidationError(
                    gettext_lazy("The All mode cannot overlap with other time periods")
                )


class ChooseOutlineTimeForm(forms.Form):
    choice = forms.ChoiceField(required=True, choices=[])

    def __init__(self, *args, **kwargs):
        super(ChooseOutlineTimeForm, self).__init__(*args, **kwargs)
        self.fields["choice"].widget.attrs["class"] = "form-control"


class CreateNewInitialTarget(forms.Form):
    target = forms.CharField(
        max_length=7,
        label="",
    )
    
    def __init__(self, *args, **kwargs):
        self.outline = kwargs.pop("outline")
        super(CreateNewInitialTarget, self).__init__(*args, **kwargs)
        self.fields["target"].widget.attrs["class"] = "form-control"

    def clean_target(self):
        coord = self.cleaned_data["target"].strip()

        if models.TargetVertex.objects.filter(
            target=coord, outline=self.outline
        ).exists():
            self.add_error("target", gettext_lazy("This village is already a target!"))
            return

        if not models.VillageModel.objects.filter(coord=coord, world=self.outline.world).exists():
            self.add_error(
                "target",
                gettext_lazy("Village with that coords did not found."),
            )
            return


class AddNewWorldForm(forms.ModelForm):
    class Meta:
        model = models.World
        fields = ["server", "postfix"]

        labels = {
            "server": gettext_lazy("Choose server"),
            "postfix": gettext_lazy("World prefix"),
        }

    def clean(self):

        server = self.cleaned_data.get("server")
        postfix = self.cleaned_data.get("postfix")
        if postfix is None:
            return None
        try:
            server = models.Server.objects.get(dns=server)
        except Exception:
            return None
        world = models.World(server=server, postfix=postfix.lower())
        world_query = database_update.WorldQuery(world=world)

        result = world_query.check_if_world_exist_and_try_create()
        if result[1] == "error":
            raise forms.ValidationError(
                gettext_lazy("Connection error, world does not exists or is archived!")
            )
        elif result[1] == "added":
            raise forms.ValidationError(gettext_lazy("World is already added!"))

        elif result[1] == "success":
            world_query.update_all()
            world_query.world.save()


class ChangeServerForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ["server"]
        labels = {"server": gettext_lazy("You can set your server:")}
