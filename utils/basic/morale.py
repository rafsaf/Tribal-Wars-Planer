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
from collections.abc import Sequence
from datetime import UTC, datetime

from base.models import Outline, WeightMaximum
from base.models import TargetVertex as Target
from utils.fast_weight_maximum import FastWeightMaximum


def _return_100():
    return 100


def generate_morale_dict(
    outline: Outline,
    target_lst: list[Target],
    weight_max_lst: Sequence[FastWeightMaximum | WeightMaximum],
) -> defaultdict[tuple[str, str], int]:
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

    target_player_to_points: dict[str, Target] = {
        target.player: target for target in target_lst
    }
    weight_player_to_points: dict[str, int] = {
        weight_max.player: weight_max.points for weight_max in weight_max_lst
    }

    for _, target in target_player_to_points.items():
        for weight_player, weight_points in weight_player_to_points.items():
            if weight_points == 0:
                continue
            if outline.world.morale == 1:
                # points based only
                morale = round(((3 * target.points / weight_points) + 0.3) * 100)
            else:
                # time-points based outline.world.morale == 2
                morale = (3 * target.points / weight_points) + 0.25
                if morale < 0.5:
                    target_player_time_played = now - target.player_created_at
                    morale += target_player_time_played.days / 500
                    morale = min(morale, 0.5)
                morale = round(morale * 100)

            if morale >= 100:
                continue
            map_player_tuple_to_morale[(target.player, weight_player)] = morale
    return map_player_tuple_to_morale
