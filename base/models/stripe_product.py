# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext as _

from tribal_wars_planer.fetch_error_manager import FetchErrorManager


class StripeProduct(models.Model):
    product_id = models.CharField(max_length=128, primary_key=True)
    active = models.BooleanField()
    name = models.CharField(max_length=512)
    updated = models.IntegerField()
    created = models.IntegerField()
    months = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)]
    )

    objects = FetchErrorManager()

    class Meta:
        ordering = ["-active", "months"]

    def __str__(self) -> str:
        if self.months == 1:
            return _("Premium 1 month")
        else:
            return _("Premium %s months") % self.months
