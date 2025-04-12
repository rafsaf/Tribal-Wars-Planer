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

"""App forms"""

import logging
import re

from django import forms
from django.conf import settings
from django.db.models.query import QuerySet
from django.forms import BaseFormSet
from django.utils.translation import gettext_lazy

from base.models.outline import Outline
from base.models.village_model import VillageModel
from utils import basic, database_update

from . import models

log = logging.getLogger(__name__)


class OutlineForm(forms.Form):
    """New Outline Form"""

    name = forms.CharField(
        max_length=24,
        label=gettext_lazy("Outline Name"),
    )
    date = forms.DateField(label=gettext_lazy("Date"), input_formats=["%Y-%m-%d"])
    world = forms.ChoiceField(choices=[], label=gettext_lazy("World"))


class OutlineDuplicateForm(forms.ModelForm):
    class Meta:
        model = models.Outline
        fields = ["name", "date", "parent_outline"]
        widgets = {
            "parent_outline": forms.HiddenInput(),
            "date": forms.DateInput(format="%Y-%m-%d"),
        }
        labels = {
            "name": gettext_lazy("Outline Name"),
            "date": gettext_lazy("Date"),
        }

    unused_troops = forms.BooleanField(
        label=gettext_lazy("Use unused troops"),
        required=False,
        initial=True,
        help_text=gettext_lazy(
            "Use unused army or deff troops from result tab from parent outline in Troops data tab"
        ),
    )


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
        self.outline: Outline = kwargs.pop("outline")
        super().__init__(*args, **kwargs)
        self.fields["off_troops"].strip = False  # type: ignore
        self.first_error_message: str = ""
        self.second_error_message: str = ""

    def clean_off_troops(self):
        """User's input from script"""
        text: str = self.cleaned_data["off_troops"]
        if text == "":
            self.add_error(field=None, error=gettext_lazy("Text cannot be empty!"))
            return None

        villages = set(
            VillageModel.objects.filter(
                player__tribe__tag__in=self.outline.ally_tribe_tag,
                world=self.outline.world,
            ).values_list("coord", flat=True)
        )
        evidence = basic.world_evidence(self.outline.world)

        already_used_villages = set()

        for i, text_line in enumerate(text.split("\r\n")):
            army = basic.Army(text_army=text_line, evidence=evidence)
            try:
                army.clean_init(villages, self.outline.ally_tribe_tag)
            except basic.ArmyError as error:
                if not self.first_error_message:
                    self.first_error_message = str(error)
                    if error.coord:
                        village = VillageModel.objects.filter(
                            coord=error.coord, world=self.outline.world
                        ).first()
                        if not village:
                            self.second_error_message = gettext_lazy(
                                "[coord: %(coord)s] - [world: %(world)s]: no such village"
                            ) % {
                                "coord": error.coord,
                                "world": self.outline.world.game_name(),
                            }

                        else:
                            self.second_error_message = gettext_lazy(
                                "[coord: %(coord)s] - "
                                "[world: %(world)s] - "
                                "[player: %(player)s] - "
                                "[tribe: %(tribe)s]"
                            ) % {
                                "coord": village.coord,
                                "world": village.world.game_name(),
                                "player": village.player,
                                "tribe": (
                                    village.player.tribe if village.player else None
                                ),
                            }
                self.add_error("off_troops", str(i))
                continue

            if army.coord in already_used_villages:
                if not self.first_error_message:
                    self.first_error_message = gettext_lazy(
                        "Village in this line is duplicated: %(coord)s"
                    ) % {"coord": army.coord}

                self.add_error("off_troops", str(i))
                continue
            else:
                already_used_villages.add(army.coord)

        return text


class DeffTroopsForm(forms.ModelForm):
    """Pasted data from defence script"""

    class Meta:
        model = models.Outline
        fields = {"deff_troops"}
        labels = {"deff_troops": gettext_lazy("Deff collection ")}
        widgets = {
            "deff_troops": forms.Textarea(
                attrs={"spellcheck": "false", "autocomplete": "off"}
            )
        }

    def __init__(self, *args, **kwargs):
        self.outline: Outline = kwargs.pop("outline")
        super().__init__(*args, **kwargs)
        self.fields["deff_troops"].strip = False  # type: ignore
        self.first_error_message: str = ""
        self.second_error_message: str = ""

    def clean_deff_troops(self):
        """User's input from script"""
        text = self.cleaned_data["deff_troops"]
        out_lines: list[str] = []

        if text == "":
            self.add_error(field=None, error=gettext_lazy("Text cannot be empty!"))
            return None

        villages = set(
            VillageModel.objects.filter(
                player__tribe__tag__in=self.outline.ally_tribe_tag,
                world=self.outline.world,
            ).values_list("coord", flat=True)
        )
        evidence = basic.world_evidence(self.outline.world)

        already_used_villages: dict[str, int] = {}
        previous_army = basic.Defence(text_army="", evidence=evidence)

        for i, text_line in enumerate(text.split("\r\n")):
            army = basic.Defence(text_army=text_line, evidence=evidence)
            try:
                army.clean_init(
                    villages, self.outline.ally_tribe_tag, previous=previous_army
                )
                out_lines.append(",".join(army.text_army))

            except basic.DefenceError as error:
                if not self.first_error_message:
                    self.first_error_message = str(error)
                    if error.coord:
                        village = VillageModel.objects.filter(
                            coord=error.coord, world=self.outline.world
                        ).first()
                        if not village:
                            self.second_error_message = gettext_lazy(
                                "[coord: %(coord)s] - [world: %(world)s]: no such village"
                            ) % {
                                "coord": error.coord,
                                "world": self.outline.world.game_name(),
                            }

                        else:
                            self.second_error_message = gettext_lazy(
                                "[coord: %(coord)s] - "
                                "[world: %(world)s] - "
                                "[player: %(player)s] - "
                                "[tribe: %(tribe)s]"
                            ) % {
                                "coord": village.coord,
                                "world": village.world.game_name(),
                                "player": village.player,
                                "tribe": (
                                    village.player.tribe if village.player else None
                                ),
                            }
                self.add_error("deff_troops", i)  # type: ignore
                continue

            previous_army = army

            if army.coord in already_used_villages:
                already_used_villages[army.coord] += 1
                if already_used_villages[army.coord] > 2:
                    if not self.first_error_message:
                        self.first_error_message = gettext_lazy(
                            "Village in this line is duplicated: %(coord)s"
                        ) % {"coord": army.coord}

                    self.add_error("deff_troops", i)  # type: ignore
            else:
                already_used_villages[army.coord] = 1
        return "\r\n".join(out_lines)


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
        super().__init__(*args, **kwargs)

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
        super().__init__(*args, **kwargs)

    def clean_target(self):
        """User's input Targets"""

        data = self.cleaned_data["target"]
        data_lines = basic.TargetsData(data=data, world=self.outline.world)
        if data == "":
            data_lines.new_validated_data = ""
        else:
            data_lines.validate()

        if len(data_lines.errors_ids) == 0:
            new_data = data_lines.new_validated_data.strip()
            if (
                self.target_mode.is_real
                and self.outline.initial_outline_targets != new_data
            ):
                self.outline.initial_outline_targets = new_data
                self.outline.save(update_fields=["initial_outline_targets"])
            elif (
                self.target_mode.is_fake
                and self.outline.initial_outline_fakes != new_data
            ):
                self.outline.initial_outline_fakes = new_data
                self.outline.save(update_fields=["initial_outline_fakes"])
            elif (
                self.target_mode.is_ruin
                and self.outline.initial_outline_ruins != new_data
            ):
                self.outline.initial_outline_ruins = new_data
                self.outline.save(update_fields=["initial_outline_ruins"])

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
            self.add_error("target", str(error_id))
        return data


class AvailableTroopsForm(forms.ModelForm):
    class Meta:
        model = models.Outline
        fields = [
            "initial_outline_min_off",
            "initial_outline_max_off",
            "initial_outline_front_dist",
            "initial_outline_target_dist",
            "initial_outline_maximum_off_dist",
            "initial_outline_excluded_coords",
        ]
        labels = {
            "initial_outline_min_off": gettext_lazy("Min. off units number"),
            "initial_outline_max_off": gettext_lazy("Max. off units number"),
            "initial_outline_front_dist": gettext_lazy(
                "Minimum distance from front line"
            ),
            "initial_outline_target_dist": gettext_lazy("Max Distance for nobles"),
            "initial_outline_maximum_off_dist": gettext_lazy(
                "Max Distance for offs and ruins"
            ),
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
            "initial_outline_maximum_off_dist": gettext_lazy(
                "Greater than or equal to 0 and less than or equal to 1000. This is STRICT limit of distance for any OFF regardless of distance from the front line."
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

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.outline: models.Outline = kwargs["instance"]
        self.fields["initial_outline_target_dist"].help_text = gettext_lazy(
            "Greater than or equal to 0 and less than or equal to your world maximum: %(max_noble_distance)s. This is STRICT limit of distance for any NOBLE regardless of distance from the front line."
        ) % {"max_noble_distance": self.outline.world.max_noble_distance}

    def clean_initial_outline_target_dist(self) -> int:
        noble_dist: int = self.cleaned_data["initial_outline_target_dist"]
        if noble_dist > self.outline.world.max_noble_distance:
            self.add_error(
                "initial_outline_target_dist",
                gettext_lazy("Ensure this value is less than or equal to %(value)s.")
                % {"value": self.outline.world.max_noble_distance},
            )
        return noble_dist

    def clean_initial_outline_excluded_coords(self):
        """Excluded Villages"""
        coords = self.cleaned_data["initial_outline_excluded_coords"]
        try:
            basic.many_villages(coords)
        except basic.VillageError as error:
            self.add_error("initial_outline_excluded_coords", str(error))
        return coords

    def clean(self):
        off_min: int | None = self.cleaned_data.get("initial_outline_min_off")
        off_max: int | None = self.cleaned_data.get("initial_outline_max_off")
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
            "send_message_with_url",
            "title_message",
            "text_message",
        ]
        labels = {
            "default_show_hidden": gettext_lazy("Show all hidden"),
            "title_message": gettext_lazy("Title of message:"),
            "text_message": gettext_lazy("Content of message:"),
            "sending_option": gettext_lazy("Sending Options:"),
            "send_message_with_url": gettext_lazy("Add links to direct messages:"),
        }
        help_texts = {
            "default_show_hidden": gettext_lazy(
                "By checking this option, players will see the commands of all other players for their own targets. By default, it’s not turned on and players only see their commands."
            ),
            "title_message": gettext_lazy("Title, maximum length 200."),
            "text_message": gettext_lazy(
                "BBCode message, maximum length 2000. Hint: Format text in game and paste here."
            ),
            "sending_option": gettext_lazy(
                "Directly messages will bahave poorly with many (more than 80-100) commands"
            ),
            "send_message_with_url": gettext_lazy(
                "If checked, direct messages from options above will have safe link to planer"
            ),
        }
        widgets = {
            "sending_option": forms.RadioSelect,
            "text_message": forms.Textarea,
        }

    set_as_default = forms.BooleanField(
        required=False,
        label=gettext_lazy("Set sending option as default choice for next outlines"),
        initial=False,
    )


class InputDataPlanerForm(forms.ModelForm):
    class Meta:
        model = models.Outline
        fields = [
            "input_data_type",
        ]
        labels = {
            "input_data_type": gettext_lazy("Input type for planer"),
        }
        help_texts = {
            "input_data_type": gettext_lazy(
                "Data for planer tab may be from Army or Defence tabs. Army - all troops (also that are outside of villages), Defence - only troops from villages."
            ),
        }
        widgets = {
            "sending_option": forms.RadioSelect,
            "text_message": forms.Textarea,
        }

    set_as_default = forms.BooleanField(
        required=False,
        label=gettext_lazy("Set as default choice for next outlines"),
        initial=False,
    )


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
            "filter_weights_nobles_min",
            "filter_card_number",
            "filter_hide_front",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["filter_weights_min"].widget.attrs["class"] = "form-control"
        self.fields["filter_weights_catapults_min"].widget.attrs["class"] = (
            "form-control"
        )
        self.fields["filter_weights_nobles_min"].widget.attrs["class"] = "form-control"
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
        super().__init__(*args, **kwargs)
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
            "initial_outline_nobles_limit",
            "initial_outline_minimum_noble_troops",
        ]
        labels = {
            "mode_off": gettext_lazy(
                "Choose the default distance of the written offs:"
            ),
            "mode_noble": gettext_lazy(
                "Choose the default distance of the written nobles:"
            ),
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
            "initial_outline_nobles_limit": gettext_lazy(
                "Max. number of nobles send per village:"
            ),
            "initial_outline_minimum_noble_troops": gettext_lazy(
                "Min. off units for every noble"
            ),
        }
        help_texts = {
            "mode_guide": gettext_lazy(
                "For 4 nobles in village, first option would <b>try</b> to send them all 4x on target X, second would randomly send from 1 to 4 nobles to single target or many targets (as needed), and last option would send 1x on X1,X2,X2,X4 (one noble per target)."
            ),
            "mode_division": gettext_lazy(
                'For 20000 troops and 4 nobles in village, first option would try to use 4 x 5000, second 1 x 19700 + 3 x 100, and last 4 x 100, where 100 can be changed in "Min. off units for every noble".'
            ),
            "initial_outline_nobles_limit": gettext_lazy(
                "Defaults to 16. Between 1 and 250. "
                "For example you may want only 4 nobles from single "
                "village or even 1 (with full off). "
                'Best works with "Min. off units for every noble" below.'
            ),
            "initial_outline_minimum_noble_troops": gettext_lazy(
                "Defaults to just 100. Must be between 0 and 28000. This is strict minimum so if village have nobles, but not enough off units, Planer won't use it. Use with caution as it can change drastically how other options behave."
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
            "initial_outline_catapult_min_value",
            "initial_outline_catapult_max_value",
            "initial_outline_off_left_catapult",
            "initial_outline_average_ruining_points",
        ]
        labels = {
            "initial_outline_catapult_min_value": gettext_lazy(
                "MIN number of catapults in one ruin attack:"
            ),
            "initial_outline_catapult_max_value": gettext_lazy(
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
        widget=forms.NumberInput,
        disabled=True,
        label=gettext_lazy("Sum of off"),
        min_value=0,
        required=False,
    )
    off_no_catapult = forms.IntegerField(
        widget=forms.NumberInput,
        label=gettext_lazy("Off without catapults"),
        min_value=0,
        help_text="0-0",
    )
    catapult = forms.IntegerField(
        widget=forms.NumberInput,
        label=gettext_lazy("Catapults"),
        min_value=0,
        help_text="0-0",
    )
    nobleman = forms.IntegerField(
        widget=forms.NumberInput,
        label=gettext_lazy("Noble"),
        min_value=0,
        help_text="0-0",
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
        super().__init__(*args, **kwargs)
        self.fields["status"].widget.attrs["class"] = "form-control"
        self.fields["unit"].widget.attrs["class"] = "form-control"
        self.fields["from_number"].widget.attrs["class"] = "form-control"
        self.fields["to_number"].widget.attrs["class"] = "form-control"
        self.fields["from_time"].widget.attrs["class"] = "time-timepicker form-control"
        self.fields["to_time"].widget.attrs["class"] = "time-timepicker form-control"

    def clean(self):  # noqa: PLR0912
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
    def clean(self):  # noqa: PLR0912
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


class ChooseOutlineTimeForm(forms.Form):
    choice = forms.ChoiceField(required=True, choices=[])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
        super().__init__(*args, **kwargs)
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

        village_query: QuerySet[models.VillageModel] = (
            models.VillageModel.objects.filter(coord=coord, world=self.outline.world)
        )
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
        world_query = database_update.WorldUpdateHandler(world=world)

        if models.World.objects.filter(
            server=world.server, postfix=world.postfix
        ).exists():
            raise forms.ValidationError(gettext_lazy("World is already added!"))

        try:
            world_query.create_or_update_config()
        except database_update.WorldOutdatedError:
            raise forms.ValidationError(
                code="does_not_exists",
                message=gettext_lazy(
                    "Connection error, world does not exists or is archived!"
                ),
            )
        except database_update.DatabaseUpdateError as err:
            log.error(
                "Error during world create_or_update_config: %s",
                err,
            )
            raise forms.ValidationError(
                code="does_not_exists",
                message=gettext_lazy(
                    "Connection error, world does not exists or is archived!"
                ),
            )

        world_query.update_all(download_try=1)
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
        fields = [
            "server",
            "currency",
            "input_data_type",
            "default_morale_on",
            "send_message_with_url",
            "sending_option",
        ]
        labels = {
            "server": gettext_lazy("Please select your server:"),
            "default_morale_on": gettext_lazy(
                "Turn on morale calculations in every outline by default:"
            ),
            "input_data_type": gettext_lazy("Default input type for planer"),
            "currency": gettext_lazy("Please select your currency:"),
            "sending_option": gettext_lazy("Sending Options:"),
            "send_message_with_url": gettext_lazy("Add links to direct messages:"),
        }
        help_texts = {
            "sending_option": gettext_lazy("Prefered sending option in Results tab"),
            "send_message_with_url": gettext_lazy(
                "If checked, direct messages in Results tab will have safe link to planer"
            ),
        }
        widgets = {
            "sending_option": forms.RadioSelect,
        }
