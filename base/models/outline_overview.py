# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

import typing

from django.core.serializers.json import DjangoJSONEncoder
from django.db import models

from base.models.outline import Outline
from tribal_wars_planer.fetch_error_manager import FetchErrorManager

if typing.TYPE_CHECKING:
    from base.models.overview import Overview


class OutlineOverview(models.Model):
    outline = models.ForeignKey(
        Outline, on_delete=models.SET_NULL, null=True, blank=True
    )
    weights_json = models.TextField(default="", blank=True)
    targets_json = models.TextField(default="", blank=True)
    world_json = models.JSONField(default=dict, blank=True, encoder=DjangoJSONEncoder)
    outline_json = models.JSONField(default=dict, blank=True, encoder=DjangoJSONEncoder)

    if typing.TYPE_CHECKING:
        overview_set: models.Manager[Overview]

    objects = FetchErrorManager()
