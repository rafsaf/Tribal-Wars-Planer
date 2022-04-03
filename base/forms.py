# Copyright 2021 Rafał Safin (rafsaf). All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

""" App forms """

import re

from django import forms
from django.conf import settings
from django.db.models.query import QuerySet
from django.forms import BaseFormSet
from django.utils.translation import gettext_lazy

from utils import basic, database_update

from . import models


class OutlineForm(forms.Form):
    """New Outline Form"""

    name = forms.CharField(
        max_length=20,
        label=gettext_lazy("Outline Name"),
        widget=forms.Textarea,
    )
    date = forms.DateField(label=gettext_lazy("Date"), input_formats=["%Y-%m-%d"])
    world = forms.ChoiceField(choices=[], label=gettext_lazy("World"))


class OffTroopsForm(forms.ModelForm):
    """Pasted data from army script"""

    class Meta:
        model = models.Outline
        fields = ["off_troops"]
        labels = {"off_troops": gettext_lazy("Army collection")}
        widgets = {
            "off_troops": forms.Textarea(
                attrs={"spellcheck": "false", "autocomplete": "off"}
            )
        }

    def __init__(self, *args, **kwargs):
        self.outline = kwargs.pop("outline")
        super(OffTroopsForm, self).__init__(*args, **kwargs)
        self.fields["off_troops"].strip = False

    def clean_off_troops(self):
        """User's input from script"""
        text = self.cleaned_data["off_troops"]
        if text == "":
            self.add_error(field=None, error=gettext_lazy("Text cannot be empty!"))
            return None

        player_dictionary = basic.coord_to_player(self.outline)
        evidence = basic.world_evidence(self.outline.world)

        already_used_villages = set()

        for i, text_line in enumerate(text.split("\r\n")):
            army = basic.Army(text_army=text_line, evidence=evidence)
            try:
                army.clean_init(player_dictionary)
            except basic.ArmyError:
                self.add_error("off_troops", i)  # type: ignore
                continue

            if army.coord in already_used_villages:
                self.add_error("off_troops", i)  # type: ignore
                continue
            else:
                already_used_villages.add(army.coord)

        return text


class DeffTroopsForm(forms.ModelForm):
    """Pasted data from defence script"""

    class Meta:
        model = models.Outline
        fields = {"deff_troops"}
        labels = {"deff_troops": gettext_lazy("Deff collection")}
        widgets = {
            "deff_troops": forms.Textarea(
                attrs={"spellcheck": "false", "autocomplete": "off"}
            )
        }

    def __init__(self, *args, **kwargs):
        self.outline = kwargs.pop("outline")
        super(DeffTroopsForm, self).__init__(*args, **kwargs)
        self.fields["deff_troops"].strip = False

    def clean_deff_troops(self):
        """User's input from script"""
        text = self.cleaned_data["deff_troops"]
        if text == "":
            self.add_error(field=None, error=gettext_lazy("Text cannot be empty!"))
            return None

        player_dictionary = basic.coord_to_player(self.outline)
        evidence = basic.world_evidence(self.outline.world)

        already_used_villages = dict()

        for i, text_line in enumerate(text.split("\r\n")):
            army = basic.Defence(text_army=text_line, evidence=evidence)
            try:
                army.clean_init(player_dictionary)
            except basic.DefenceError:
                self.add_error("deff_troops", i)  # type: ignore
                continue
            if army.coord in already_used_villages:
                already_used_villages[army.coord] += 1
                if already_used_villages[army.coord] > 2:
                    self.add_error("deff_troops", i)  # type: ignore
            else:
                already_used_villages[army.coord] = 1

        return text


class MyTribeTagForm(forms.Form):
    """Add ally tribes to outline"""

    tribe1 = forms.ChoiceField(
        choices=[], label=gettext_lazy("Ally tribe"), required=False
    )

    def clean_tribe1(self):
        """User's tags input"""
        plemie = self.cleaned_data["tribe1"]
        if plemie == "banned":
            self.add_error("tribe1", gettext_lazy("Select tribe from list"))
            return None
        return plemie


class EnemyTribeTagForm(forms.Form):
    """Add enemy tribes to outline"""

    tribe2 = forms.ChoiceField(
        choices=[], label=gettext_lazy("Enemy tribe"), required=False
    )

    def clean_tribe2(self):
        """User's tag input"""
        plemie = self.cleaned_data["tribe2"]
        if plemie == "banned":
            self.add_error("tribe2", gettext_lazy("Select tribe from list"))
            return None
        return plemie


class GetDeffForm(forms.Form):
    """GetDeff function"""

    radius = forms.IntegerField(
        min_value=0,
        max_value=1000,
        label=gettext_lazy("Radius"),
        widget=forms.NumberInput,
        help_text=gettext_lazy(
            "Greater than or equal to 0 and less than or equal to 1000."
        ),
        initial=15,
    )

    excluded = forms.CharField(
        max_length=3000,
        widget=forms.Textarea,
        label=gettext_lazy("Excluded enemy villages"),
        required=False,
        help_text=gettext_lazy("Exact coords separated by a space or an entry."),
    )

    def __init__(self, *args, **kwargs):
        self.world = kwargs.pop("world")
        super(GetDeffForm, self).__init__(*args, **kwargs)

    def clean_excluded(self):
        """Excluded Villages"""
        villages = self.cleaned_data["excluded"]
        try:
            basic.many_villages(self.cleaned_data["excluded"])
        except basic.VillageError as error:
            self.add_error("excluded", str(error))
            return None
        return villages


class InitialOutlineForm(forms.Form):
    """New Initial Outline"""

    target = forms.CharField(
        max_length=130000,
        widget=forms.Textarea,
        label=gettext_lazy("Targets"),
        required=False,
        strip=False,
    )

    def __init__(self, *args, **kwargs):
        self.outline: models.Outline = kwargs.pop("outline")
        self.target_mode: basic.TargetMode = kwargs.pop("target_mode")
        self.max_to_add: int = kwargs.pop(
            "max_to_add", settings.INPUT_OUTLINE_MAX_TARGETS
        )
        super(InitialOutlineForm, self).__init__(*args, **kwargs)

    def clean_target(self):
        """User's input Targets"""

        data = self.cleaned_data["target"]
        data_lines = basic.TargetsData(data=data, world=self.outline.world)
        if data == "":
            data_lines.new_validated_data = ""
        else:
            data_lines.validate()

        if len(data_lines.errors_ids) == 0:
            if self.target_mode.is_real:
                self.outline.initial_outline_targets = (
                    data_lines.new_validated_data.strip()
                )
            elif self.target_mode.is_fake:
                self.outline.initial_outline_fakes = (
                    data_lines.new_validated_data.strip()
                )
            else:
                self.outline.initial_outline_ruins = (
                    data_lines.new_validated_data.strip()
                )
            self.outline.save()
        if len(data_lines.lines) > self.max_to_add:
            self.add_error(
                None,
                gettext_lazy(
                    "You are trying to mantain more than %s targets in total - that is global limit for targets number.<br> Please decrease the total number of targets."
                )
                % settings.INPUT_OUTLINE_MAX_TARGETS,
            )
            return data

        for error_id in data_lines.errors_ids:
            self.add_error("target", error_id)
        return data


class AvailableTroopsForm(forms.ModelForm):
    class Meta:
        model = models.Outline
        fields = [
            "initial_outline_min_off",
            "initial_outline_max_off",
            "initial_outline_front_dist",
            "initial_outline_maximum_front_dist",
            "initial_outline_target_dist",
            "initial_outline_excluded_coords",
        ]
        labels = {
            "initial_outline_min_off": gettext_lazy("Min. off units number"),
            "initial_outline_max_off": gettext_lazy("Max. off units number"),
            "initial_outline_front_dist": gettext_lazy(
                "Minimum distance from front line"
            ),
            "initial_outline_maximum_front_dist": gettext_lazy(
                "Maximum distance from front line"
            ),
            "initial_outline_target_dist": gettext_lazy("Max Distance for nobles"),
        }
        help_texts = {
            "initial_outline_min_off": gettext_lazy(
                "Greater than or equal to 1 and less than or equal to 28000. Only offs above this value will be considered full offs and will be written out."
            ),
            "initial_outline_max_off": gettext_lazy(
                "Defaults to 28000. Similar to minimum off units number, must be greater than it."
            ),
            "initial_outline_front_dist": gettext_lazy(
                "Greater than or equal to 0 and less than or equal to 500. Villages closer to the enemy than this value will be considered front-line and not written out by default."
            ),
            "initial_outline_maximum_front_dist": gettext_lazy(
                "Greater than or equal to 0 and less than or equal to 1000. Villages farther from the enemy than this value will be considered too far from the front and completely skipped."
            ),
            "initial_outline_target_dist": gettext_lazy(
                "Greater than or equal to 0 and less than or equal to 1000."
            ),
        }

    initial_outline_excluded_coords = forms.CharField(
        label=gettext_lazy("Excluded enemy villages coords (secluded villages)"),
        required=False,
        max_length=100000,
        initial="",
        help_text=gettext_lazy("Exact coords separated by a space or an entry"),
        widget=forms.Textarea,
    )

    def clean_initial_outline_excluded_coords(self):
        """Excluded Villages"""
        coords = self.cleaned_data["initial_outline_excluded_coords"]
        try:
            basic.many_villages(coords)
        except basic.VillageError as error:
            self.add_error("initial_outline_excluded_coords", str(error))
        return coords

    def clean(self):
        radius_min: int | None = self.cleaned_data.get("initial_outline_front_dist")
        radius_max: int | None = self.cleaned_data.get(
            "initial_outline_maximum_front_dist"
        )
        off_min: int | None = self.cleaned_data.get("initial_outline_min_off")
        off_max: int | None = self.cleaned_data.get("initial_outline_max_off")
        if radius_min is not None and radius_max is not None:
            if radius_min > radius_max:
                self.add_error(
                    "initial_outline_front_dist",
                    f"It cannot be grater than maximum! Change this value to less than {radius_max} or increase the maximum.",
                )
                self.add_error(
                    "initial_outline_maximum_front_dist",
                    f"It cannot be less than minimum! Change this value to greater than {radius_min} or reduce the minimum.",
                )
        if off_min is not None and off_max is not None:
            if off_min > off_max:
                self.add_error(
                    "initial_outline_min_off",
                    f"It cannot be grater than maximum! Change this value to less than {off_max} or increase the maximum.",
                )
                self.add_error(
                    "initial_outline_max_off",
                    f"It cannot be less than minimum! Change this value to greater than {off_min} or reduce the minimum.",
                )

        return super().clean()


class SettingMessageForm(forms.ModelForm):
    class Meta:
        model = models.Outline
        fields = [
            "default_show_hidden",
            "sending_option",
            "title_message",
            "text_message",
        ]
        labels = {
            "default_show_hidden": gettext_lazy("Show all hidden"),
            "title_message": gettext_lazy("Title of message:"),
            "text_message": gettext_lazy("Content of message:"),
            "sending_option": gettext_lazy("Sending Options:"),
        }
        help_texts = {
            "default_show_hidden": gettext_lazy(
                "By checking this option, players will see the commands of all other players for their own targets. By default, it's not turned on and players only see their commands."
            ),
            "title_message": gettext_lazy("Maximum length: 200."),
            "text_message": gettext_lazy("Maximum length: 2000."),
            "sending_option": gettext_lazy(
                "Directly messages will bahave poorly with many (more than 80-100) commands"
            ),
        }
        widgets = {
            "sending_option": forms.RadioSelect,
            "text_message": forms.Textarea,
        }


class SettingDateForm(forms.ModelForm):
    class Meta:
        model = models.Outline
        fields = ["date"]

    date = forms.DateField(
        label=gettext_lazy("Set new date"), input_formats=["%Y-%m-%d"]
    )


class SetNewOutlineFilters(forms.ModelForm):
    class Meta:
        model = models.Outline
        fields = [
            "filter_weights_min",
            "filter_weights_max",
            "filter_weights_catapults_min",
            "filter_card_number",
            "filter_hide_front",
        ]

    def __init__(self, *args, **kwargs):
        super(SetNewOutlineFilters, self).__init__(*args, **kwargs)
        self.fields["filter_weights_min"].widget.attrs["class"] = "form-control"
        self.fields["filter_weights_catapults_min"].widget.attrs[
            "class"
        ] = "form-control"
        self.fields["filter_weights_max"].widget.attrs["class"] = "form-control"
        self.fields["filter_card_number"].widget.attrs["class"] = "form-control"
        self.fields["filter_hide_front"].widget.attrs["class"] = "form-control"


class SetTargetsMenuFilters(forms.ModelForm):
    class Meta:
        model = models.Outline
        fields = [
            "filter_targets_number",
            "simple_textures",
        ]

    def __init__(self, *args, **kwargs):
        super(SetTargetsMenuFilters, self).__init__(*args, **kwargs)
        self.fields["filter_targets_number"].widget.attrs["class"] = "form-control"
        self.fields["simple_textures"].widget.attrs["class"] = "form-check-input"


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
            "initial_outline_fake_mode",
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
            "initial_outline_fake_mode": gettext_lazy(
                "Determine which villages to write fake attacks from:"
            ),
        }
        widgets = {
            "mode_off": forms.RadioSelect,
            "mode_noble": forms.RadioSelect,
            "mode_division": forms.RadioSelect,
            "mode_split": forms.RadioSelect,
            "mode_guide": forms.RadioSelect,
        }


class RuiningOutlineForm(forms.ModelForm):
    class Meta:
        model = models.Outline
        fields = [
            "initial_outline_catapult_default",
            "initial_outline_off_left_catapult",
            "initial_outline_average_ruining_points",
        ]
        labels = {
            "initial_outline_catapult_default": gettext_lazy(
                "MAX number of catapults in one ruin attack:"
            ),
            "initial_outline_off_left_catapult": gettext_lazy(
                "Number of catapults that will always be left in full offs:"
            ),
            "initial_outline_average_ruining_points": gettext_lazy(
                "How many points on average do demolished targets have:"
            ),
        }


class MoraleOutlineForm(forms.ModelForm):
    class Meta:
        model = models.Outline
        fields = [
            "morale_on_targets_greater_than",
            "morale_on",
        ]
        labels = {
            "morale_on_targets_greater_than": gettext_lazy(
                "Only attackers ABOVE this morale value can be used:"
            ),
            "morale_on": gettext_lazy("Is morale calculation active in this outline:"),
        }


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


class NightBonusSetForm(forms.ModelForm):
    class Meta:
        model = models.Outline
        fields = [
            "night_bonus",
            "enter_t1",
            "enter_t2",
        ]

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
                self.add_error(
                    "enter_t1",
                    gettext_lazy("First value must be less or equal to second!"),
                )


class WeightForm(forms.Form):
    """Change weight model"""

    weight_id = forms.IntegerField(widget=forms.HiddenInput)
    off = forms.IntegerField(
        widget=forms.NumberInput, label=gettext_lazy("Off"), min_value=0
    )
    nobleman = forms.IntegerField(
        widget=forms.NumberInput, label=gettext_lazy("Noble"), min_value=0
    )


class PeriodForm(forms.ModelForm):
    """One Period for OutlineTime"""

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
        if time1 is None:
            self.add_error("from_time", "None")
        if time2 is None:
            self.add_error("to_time", "None")
        if time1 is not None and time2 is not None and time2 < time1:
            self.add_error("from_time", "time2<time1")
            self.add_error("to_time", "time2<time1")
        if status in {"random", None}:
            if number1 is None:
                self.add_error("from_number", "None")
            if number2 is None:
                self.add_error("to_number", "None")
            try:
                greater_is_smaller = bool(number2 < number1)  # type: ignore
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
    CHOICES = [("real", "real"), ("fake", "fake"), ("ruin", "ruin")]

    target = forms.CharField(
        max_length=7,
        label="",
    )
    target_type = forms.ChoiceField(widget=forms.HiddenInput, choices=CHOICES)

    def __init__(self, *args, **kwargs):
        self.outline: models.Outline = kwargs.pop("outline")
        self.is_premium: bool = kwargs.pop("is_premium")
        super(CreateNewInitialTarget, self).__init__(*args, **kwargs)
        self.fields["target"].widget.attrs["class"] = "form-control"

    def clean_target(self):
        coord: str = self.cleaned_data["target"]
        coord = coord.strip()
        count: int = models.TargetVertex.objects.filter(outline=self.outline).count()
        if not self.is_premium and count >= settings.PREMIUM_ACCOUNT_MAX_TARGETS_FREE:
            self.add_error(
                "target",
                gettext_lazy("You need a premium account to add more targets here."),
            )
            return

        village_query: QuerySet[
            models.VillageModel
        ] = models.VillageModel.objects.filter(coord=coord, world=self.outline.world)
        if not village_query.exists():
            self.add_error(
                "target",
                gettext_lazy("Village with that coords did not found."),
            )
            return
        if not len(village_query) == 1:
            self.add_error(
                "target",
                gettext_lazy(
                    "Found more than one village in database, this is the bug. Write me: <rafal.safin@rafsaf.pl>"
                ),
            )
            return
        village: models.VillageModel = village_query[0]
        if village.player is None:
            self.add_error("target", gettext_lazy("Village must not be barbarian."))
            return


class AddNewWorldForm(forms.ModelForm):
    class Meta:
        model = models.World
        fields = ["server", "postfix"]

        labels = {
            "server": gettext_lazy("Choose server"),
            "postfix": gettext_lazy("World prefix"),
        }

    def clean_postfix(self):
        postfix: str | None = self.cleaned_data.get("postfix")
        if postfix:
            re_pattern = re.compile(r"[\w]*")
            match = re_pattern.fullmatch(postfix)
            if match is None:
                raise forms.ValidationError(
                    gettext_lazy(
                        "Unallowed symbols in postfix field! Are you sure it is valid?"
                    )
                )
        return postfix

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
        labels = {
            "server": gettext_lazy("Please select your server:"),
        }


class ChangeProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ["server", "currency", "default_morale_on"]
        labels = {
            "server": gettext_lazy("Please select your server:"),
            "default_morale_on": gettext_lazy(
                "Turn on morale calculations in every outline by default:"
            ),
            "currency": gettext_lazy("Please select your currency:"),
        }
