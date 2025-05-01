from django import forms
from django.forms import BaseFormSet, formset_factory

from base.models.overview import Overview

MAX_OVERVIEWS = 10


# Form for creating a new Shipment (only name)
class ShipmentCreateForm(forms.Form):
    name = forms.CharField(max_length=24)


# Form for entering overview tokens (used in formset)
class ShipmentOverviewTokenForm(forms.Form):
    token = forms.CharField(max_length=100, label=False)


class BaseShipmentOverviewTokenFormSet(BaseFormSet):
    def clean(self):
        super().clean()
        tokens = []
        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):  # type: ignore
                continue
            token = form.cleaned_data.get("token")
            if not Overview.objects.filter(token=token).exists():
                form.add_error("token", "")
                raise forms.ValidationError(f"Invalid overview token: {token}")
            tokens.append(token)

        if not tokens:
            raise forms.ValidationError("At least one overview token is required.")
        if len(tokens) > MAX_OVERVIEWS:
            raise forms.ValidationError(f"Maximum {MAX_OVERVIEWS} overviews allowed.")
        if len(tokens) != len(set(tokens)):
            raise forms.ValidationError("Duplicate overview tokens are not allowed.")


ShipmentOverviewTokenFormSet = formset_factory(
    ShipmentOverviewTokenForm,  # type: ignore
    formset=BaseShipmentOverviewTokenFormSet,
    extra=0,
    min_num=1,
    max_num=MAX_OVERVIEWS,
    can_delete=True,
)
