# Copyright 2025 Rafał Safin (rafsaf). All Rights Reserved.
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

from django import forms
from django.forms import BaseFormSet, formset_factory
from django.utils.translation import gettext_lazy

from base.models.overview import Overview

MAX_OVERVIEWS = 10


# Form for creating a new Shipment (only name)
class ShipmentCreateForm(forms.Form):
    name = forms.CharField(max_length=24, label=gettext_lazy("Name"))


# Form for entering overview tokens (used in formset)
class ShipmentOverviewTokenForm(forms.Form):
    token = forms.CharField(max_length=100, label="")


class BaseShipmentOverviewTokenFormSet(BaseFormSet):
    def clean(self):
        super().clean()
        tokens = []
        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):  # type: ignore
                continue
            if form.errors:
                return

            token = form.cleaned_data.get("token")

            if not Overview.objects.filter(token=token).exists():
                form.add_error("token", "")
                raise forms.ValidationError(
                    gettext_lazy("Invalid overview token: %(token)s") % {"token": token}
                )
            tokens.append(token)

        if len(tokens) != len(set(tokens)):
            raise forms.ValidationError(
                gettext_lazy("Duplicate overview tokens are not allowed.")
            )


ShipmentOverviewTokenFormSet = formset_factory(
    ShipmentOverviewTokenForm,  # type: ignore
    formset=BaseShipmentOverviewTokenFormSet,
    extra=0,
    min_num=1,
    max_num=MAX_OVERVIEWS,
    can_delete=True,
    validate_min=True,
    validate_max=True,
)
