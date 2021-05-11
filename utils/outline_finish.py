from django.utils.translation import gettext as _
import secrets
import json
from typing import Dict, List, Optional, Set
from utils.basic import info_generatation
from base.models import (
    Outline,
    OutlineOverview,
    Overview,
    PeriodModel,
    Result,
    TargetVertex,
    WeightMaximum,
    WeightModel,
    Player,
    VillageModel,
)
from utils import basic
from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.query import QuerySet


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
        self.outline: Outline = outline
        self.target_msg: str = _("Target")
        self.village_msg: str = _("Village")
        self.player_msg: str = _("Player")
        self.not_exist_msg: str = _("does not exists")
        self.error_messages_set: Set[str] = set()
        self.player_id_dictionary: Dict[str, str] = dict()
        self.village_id_dictionary: Dict[str, str] = dict()
        self.target_period_dict: Dict[TargetVertex, List[PeriodModel]] = dict()
        self.queries: basic.TargetWeightQueries = basic.TargetWeightQueries(
            outline=outline, every=True, only_with_weights=True
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
        enemy_id: Optional[str] = self.village_id_dictionary.get(target)
        if enemy_id is None:
            self._add_target_error(target)
            raise OutdatedData
        return enemy_id

    def _ally_id(self, village: str) -> str:
        ally_id: Optional[str] = self.village_id_dictionary.get(village)
        if ally_id is None:
            self._add_village_error(village)
            raise OutdatedData
        return ally_id

    def _player_id(self, player: str) -> str:
        player_id: Optional[str] = self.player_id_dictionary.get(player)
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

        player: Dict[str, str]
        for player in players:
            self.player_id_dictionary[player["name"]] = str(player["player_id"])

    def _calculate_villages_id_dictionary(self) -> None:
        distinct_weight_coords = list(
            WeightModel.objects.filter(target__in=self.queries.targets)
            .distinct("start")
            .values_list("start", flat=True)
        ) + [target.target for target in self.queries.targets]
        # coord - village_id

        villages = VillageModel.objects.filter(
            coord__in=distinct_weight_coords, world=self.outline.world
        ).values("coord", "village_id")

        village: Dict[str, str]
        for village in villages.iterator():
            self.village_id_dictionary[village["coord"]] = str(village["village_id"])

    @staticmethod
    def _weights_list(target: TargetVertex) -> "QuerySet[WeightModel]":
        return (
            WeightModel.objects.filter(target=target)
            .select_related("target", "state")
            .order_by("order")
        )

    def _time_periods(self, target: TargetVertex) -> basic.FromPeriods:
        periods_list = self.target_period_dict[target]
        time_periods = basic.FromPeriods(
            periods=periods_list, world=self.outline.world, date=self.outline.date
        )
        return time_periods

    @staticmethod
    def _json_weight(weight: WeightModel):
        return model_to_dict(
            weight,
            fields=[
                "start",
                "player",
                "off",
                "nobleman",
                "catapult",
                "ruin",
                "distance",
                "t1",
                "t2",
            ],
        )

    def _outline_overview(
        self, json_weight_dict: str, json_targets: str
    ) -> OutlineOverview:
        outline_overview = OutlineOverview.objects.create(
            outline=self.outline,
            weights_json=json_weight_dict,
            targets_json=json_targets,
        )
        return outline_overview

    def _calculate_period_dictionary(self) -> None:
        # target - lst[period1, period2, ...]
        self.target_period_dict = self.queries.target_period_dictionary()

    def __call__(self) -> Set[str]:
        self._calculate_player_id_dictionary()
        self._calculate_villages_id_dictionary()
        self._calculate_period_dictionary()

        json_weights = {}
        outline_info = basic.OutlineInfo(outline=self.outline)
        text = basic.TableText(world=self.outline.world)

        with text:
            target: TargetVertex
            for target in self.queries.targets:
                time_periods = self._time_periods(target)
                json_weights[target.pk] = list()

                lst = self._weights_list(target)
                info_line = info_generatation.TargetCount(target, lst)
                outline_info.add_target_info(info_line.line, info_line.target_type)

                weight: WeightModel
                for weight in lst:
                    weight = time_periods.next(weight=weight)
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
                        fake=target.fake,
                        deputy=deputy_id,
                    )
                    weight.t1 = weight.t1.time()
                    weight.t2 = weight.t2.time()
                    json_weights[target.pk].append(self._json_weight(weight))

        result_instance: Result = Result.objects.get(outline=self.outline)
        result_instance.results_outline = text.get_full_result()
        result_instance.results_players = outline_info.generate_nicks()
        result_instance.results_sum_up = outline_info.show_sum_up()
        result_instance.results_export = outline_info.show_export_troops()
        result_instance.save()
        json_weight_dict = json.dumps(json_weights, cls=DjangoJSONEncoder)
        json_targets = self.queries.targets_json_format()

        outline_overview = self._outline_overview(json_weight_dict, json_targets)
        overviews = []

        for player, table, string, deputy, extended in text.iterate_over():
            token = secrets.token_urlsafe()

            overviews.append(
                Overview(
                    outline=self.outline,
                    player=player,
                    token=token,
                    outline_overview=outline_overview,
                    table=table,
                    extended=extended,
                    string=string,
                    deputy=deputy,
                    show_hidden=self.outline.default_show_hidden,
                )
            )
        Overview.objects.bulk_create(overviews)
        return self.error_messages_set
