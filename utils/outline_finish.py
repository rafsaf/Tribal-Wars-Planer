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

import json
import logging
import secrets
from typing import Any

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.db.models.query import QuerySet
from django.forms.models import model_to_dict
from django.utils.translation import gettext as _

import metrics
from base import models
from base.models import (
    Outline,
    OutlineOverview,
    OutlineTime,
    Overview,
    PeriodModel,
    Player,
    Result,
    TargetVertex,
    VillageModel,
    WeightMaximum,
    WeightModel,
)
from utils import basic
from utils.basic import Unit, info_generatation

log = logging.getLogger(__name__)


class OutdatedData(Exception):
    """Raised when village or player are delted permanently from db"""


class MakeFinalOutline:
    """
    The final step in creating outline, returns set with error messages (if any occured)

    After calculating usefull dicts, (for village_id, player_id, periods)

    Main loop iterates over TARGETS

    1. take list of WeightModel for that Target
    2. add any info about weights and target to json data and "text" object

    Creating outline_overview model with json long content with all data about outline
     Update "Result" (one-to-one to outline) with usefull collected statistics

    Then we create unique links for each player which appeared earlier
     using secretes library with content from "text" for that player

    Finally return set with errors if any occured
    """

    def __init__(self, outline: Outline) -> None:
        self.target_msg = _("Target")
        self.village_msg = _("Village")
        self.player_msg = _("Player")
        self.not_exist_msg = _("does not exists")

        self.outline: Outline = outline
        self.error_messages_set: set[str] = set()
        self.player_id_dictionary: dict[str, str] = {}
        self.village_id_dictionary: dict[str, str] = {}
        self.target_period_dict: dict[TargetVertex, list[PeriodModel]] = {}

        self.targets: QuerySet[TargetVertex] = (
            (
                TargetVertex.objects.select_related("outline_time")
                .prefetch_related(
                    "weightmodel_set",
                )
                .filter(outline=outline)
                .order_by("id")
            )
            .annotate(num_of_weights=Count("weightmodel"))
            .filter(num_of_weights__gt=0)
        )

    def _add_target_error(self, target: str) -> None:
        self.error_messages_set.add(f"{self.target_msg} {target} {self.not_exist_msg}")

    def _add_village_error(self, village: str) -> None:
        self.error_messages_set.add(
            f"{self.village_msg} {village} {self.not_exist_msg}"
        )

    def _add_player_error(self, player: str) -> None:
        self.error_messages_set.add(f"{self.player_msg} {player} {self.not_exist_msg}")

    def _enemy_id(self, target: str) -> str:
        enemy_id: str | None = self.village_id_dictionary.get(target)
        if enemy_id is None:
            self._add_target_error(target)
            raise OutdatedData
        return enemy_id

    def _ally_id(self, village: str) -> str:
        ally_id: str | None = self.village_id_dictionary.get(village)
        if ally_id is None:
            self._add_village_error(village)
            raise OutdatedData
        return ally_id

    def _player_id(self, player: str) -> str:
        player_id: str | None = self.player_id_dictionary.get(player)
        if player_id is None:
            self._add_player_error(player)
            raise OutdatedData
        return player_id

    def _calculate_player_id_dictionary(self) -> None:
        distinct_player_names = (
            WeightMaximum.objects.filter(outline=self.outline)
            .distinct("player")
            .values_list("player", flat=True)
        )
        players = Player.objects.filter(
            name__in=distinct_player_names, world=self.outline.world
        ).values("name", "player_id")

        player: dict[str, str]
        for player in players:
            self.player_id_dictionary[player["name"]] = str(player["player_id"])

    def _calculate_villages_id_dictionary(self) -> None:
        distinct_weight_coords = list(
            WeightModel.objects.filter(target__in=self.targets)
            .distinct("start")
            .values_list("start", flat=True)
        ) + [target.target for target in self.targets]
        # coord - village_id

        villages = VillageModel.objects.filter(
            coord__in=distinct_weight_coords, world=self.outline.world
        ).values("coord", "village_id")

        village: dict[str, str]
        for village in villages.iterator():
            self.village_id_dictionary[village["coord"]] = str(village["village_id"])

    @staticmethod
    def _weights_list(target: TargetVertex) -> list[WeightModel]:
        return sorted(
            (target for target in target.weightmodel_set.all()),
            key=lambda target: target.order,
        )

    def _time_periods(self, target: TargetVertex) -> basic.FromPeriods:
        periods_list = self.target_period_dict[target]
        time_periods = basic.FromPeriods(
            periods=periods_list, world=self.outline.world, date=self.outline.date
        )
        return time_periods

    @staticmethod
    def _json_weight(weight: WeightModel):
        return {
            "id": weight.pk,
            "start": weight.start,
            "player": weight.player,
            "off": weight.off,
            "nobleman": weight.nobleman,
            "catapult": weight.catapult,
            "ruin": weight.ruin,
            "distance": weight.distance,
            "time_seconds": round(
                weight.distance
                / weight.state.outline.world.speed_world
                / weight.state.outline.world.speed_units
                * Unit("ram").speed
                if weight.nobleman == 0
                else Unit("nobleman").speed * 60
            ),
            "t1": weight.t1.replace(tzinfo=None),
            "t2": weight.t2.replace(tzinfo=None),
            "delivery_t1": weight.t1,
            "delivery_t2": weight.t2,
            "shipment_t1": weight.sh_t1,
            "shipment_t2": weight.sh_t2,
        }

    def _outline_overview(
        self, json_weight_dict: str, json_targets: str
    ) -> OutlineOverview:
        outline_overview = OutlineOverview.objects.create(
            outline=self.outline,
            weights_json=json_weight_dict,
            targets_json=json_targets,
            world_json={
                "id": self.outline.world.pk,
                "full_game_name": self.outline.world.full_game_name,
                "server": self.outline.world.server.dns,
                "name": str(self.outline.world),
                "speed_world": self.outline.world.speed_world,
                "speed_units": self.outline.world.speed_units,
            },
            outline_json=model_to_dict(self.outline, fields=["id", "date"]),
        )

        return outline_overview

    def _calculate_period_dictionary(self) -> None:
        # target - lst[period1, period2, ...]
        self.target_period_dict = self.target_period_dictionary()

    def __call__(self) -> set[str]:
        self._calculate_player_id_dictionary()
        self._calculate_villages_id_dictionary()
        self._calculate_period_dictionary()

        json_weights: dict[int, list[dict[str, Any]]] = {}
        outline_info = basic.OutlineInfo(outline=self.outline)
        text = basic.TableText(outline=self.outline)

        weight_lst: list[WeightModel] = []
        with text:
            target: TargetVertex
            for target in self.targets:
                time_periods = self._time_periods(target)
                json_weights[target.pk] = []

                lst = self._weights_list(target)
                info_line = info_generatation.TargetCount(target, lst)
                outline_info.add_target_info(target_info=info_line)

                time_periods.adjust_time(lst)

                for weight in lst:
                    time_periods.next(weight=weight)

                lst.sort(
                    key=lambda weight: (
                        weight.t1,
                        weight.nobleman > 0,
                        weight.t2,
                        weight.start,
                    )
                )

                for weight in lst:
                    weight_lst.append(weight)
                    json_weights[target.pk].append(self._json_weight(weight))

            text.create_weights(weight_lst)

            for weight in weight_lst:
                try:
                    ally_id = self._ally_id(weight.start)
                    enemy_id = self._enemy_id(weight.target.target)
                    deputy_id = self._player_id(weight.player)
                except OutdatedData:
                    continue
                text.add_weight(
                    weight=weight,
                    ally_id=ally_id,
                    enemy_id=enemy_id,
                    fake=weight.target.fake,
                    deputy=deputy_id,
                )

        result_instance: Result = Result.objects.get(outline=self.outline)
        result_instance.results_outline = text.get_full_result()
        result_instance.results_players = outline_info.generate_nicks()
        result_instance.results_sum_up = outline_info.show_sum_up()
        result_instance.results_export = outline_info.show_export_troops()
        result_instance.save()
        json_weight_dict = json.dumps(json_weights, cls=DjangoJSONEncoder)
        json_targets = self.targets_json_format()

        outline_overview = self._outline_overview(json_weight_dict, json_targets)
        overviews = []

        for (
            player,
            table,
            string,
            deputy,
            extended,
            new_extended,
        ) in text.iterate_over():
            token = secrets.token_urlsafe()

            overviews.append(
                Overview(
                    outline=self.outline,
                    player=player,
                    token=token,
                    outline_overview=outline_overview,
                    table=table,
                    extended=extended,
                    new_extended=new_extended,
                    string=string,
                    deputy=deputy,
                    show_hidden=self.outline.default_show_hidden,
                )
            )
        Overview.objects.bulk_create(overviews)
        return self.error_messages_set

    def targets_json_format(self):
        context = {}
        target: models.TargetVertex
        for target in self.targets:
            context[target.pk] = {
                "id": target.pk,
                "target": target.target,
                "player": target.player,
                "fake": target.fake,
                "ruin": target.ruin,
            }
        return json.dumps(context)

    def target_period_dictionary(self):
        result_dict: dict[TargetVertex, list[PeriodModel]] = {}
        outline_time_dict: dict[OutlineTime, list[PeriodModel]] = {}

        for target in self.targets:
            if target.outline_time is None:
                err = f"outline time None, {target}, {self.outline}"
                log.error(err)
                metrics.ERRORS.labels("queries_outline_time_none").inc()
                raise ValueError(err)

            outline_time_dict[target.outline_time] = []

        periods = (
            models.PeriodModel.objects.select_related("outline_time")
            .filter(outline_time__in=[target.outline_time for target in self.targets])
            .order_by("from_time", "-unit")
        )

        for period in periods:
            outline_time_dict[period.outline_time].append(period)

        for target in self.targets:
            result_dict[target] = outline_time_dict[target.outline_time]  # type: ignore

        return result_dict
