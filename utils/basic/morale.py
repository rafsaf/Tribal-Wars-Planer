# Copyright 2023 Rafał Safin (rafsaf). All Rights Reserved.
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

from collections import defaultdict
from datetime import UTC, datetime

from django.db.models.query import QuerySet

from base.models import Outline, WeightMaximum
from base.models import TargetVertex as Target


def _return_100():
    return 100


def generate_morale_dict(outline: Outline) -> defaultdict[tuple[str, str], int]:
    """
    For given outline function returns defaultdict where keys are
    tuples (DEFENDER NICK, ATACKER NICK) and values are morale between 25 and 100
    (for an attacker attacking defender)

    Defaults to 100 morale for example where some players are missing or when
    they have 0 points.
    """
    now = datetime.now(UTC)
    map_player_tuple_to_morale: defaultdict[tuple[str, str], int] = defaultdict(
        _return_100
    )
    if outline.world.morale == 0:
        return map_player_tuple_to_morale

    targets_unique_by_player = (
        Target.objects.filter(outline=outline).order_by("player").distinct("player")
    )
    weight_max_players_queryset: QuerySet[WeightMaximum] = (
        WeightMaximum.objects.filter(outline=outline)
        .order_by("player")
        .distinct("player")
    )
    unique_weight_max_players = [
        weight.player for weight in weight_max_players_queryset
    ]
    dict_player_to_points: dict[str, int] = {}

    for weight_max in weight_max_players_queryset:
        dict_player_to_points[weight_max.player] = weight_max.points

    for target in targets_unique_by_player:
        for weight_player in unique_weight_max_players:
            weight_player_points = dict_player_to_points[weight_player]
            if weight_player_points == 0:
                continue
            if outline.world.morale == 1:
                # points based only
                morale = round(((3 * target.points / weight_player_points) + 0.3) * 100)
            else:
                # time-points based outline.world.morale == 2
                morale = (3 * target.points / weight_player_points) + 0.25
                if morale < 0.5:
                    target_player_time_played = now - target.player_created_at
                    morale += target_player_time_played.days / 500
                    if morale > 0.5:
                        morale = 0.5
                morale = round(morale * 100)

            if morale >= 100:
                continue
            map_player_tuple_to_morale[(target.player, weight_player)] = morale
    return map_player_tuple_to_morale
