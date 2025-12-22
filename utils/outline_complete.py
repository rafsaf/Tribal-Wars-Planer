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

import queue
import threading
import typing
from collections import defaultdict
from collections.abc import Generator
from copy import deepcopy
from secrets import SystemRandom

from django.db import connections

from base.models import Outline, WeightMaximum, WeightModel
from base.models import TargetVertex as Target
from utils.basic import generate_morale_dict
from utils.fast_weight_maximum import FastWeightMaximum
from utils.write_noble_target import WriteNobleTarget
from utils.write_ram_target import WriteRamTarget

if typing.TYPE_CHECKING:
    from numpy.typing import NDArray


class WeightCreateThread(threading.Thread):
    def __init__(self, weight_create_queue: queue.Queue[WeightModel | None]) -> None:
        super().__init__()
        self.weight_create_queue = weight_create_queue

    def run(self) -> None:
        connections.close_all()
        weight_create_lst: list[WeightModel] = []

        while True:
            weight = self.weight_create_queue.get()
            if weight is None:
                self.weight_create_queue.task_done()
                break
            weight_create_lst.append(weight)
            if len(weight_create_lst) >= 500:
                WeightModel.objects.bulk_create(weight_create_lst)
                weight_create_lst = []
            self.weight_create_queue.task_done()

        WeightModel.objects.bulk_create(weight_create_lst)
        connections.close_all()


def generate_distance_matrix(
    weight_max_lst: list[FastWeightMaximum], targets: list[Target]
) -> tuple["NDArray | None", dict[tuple[int, int], int]]:
    import numpy as np
    from scipy.spatial.distance import cdist

    """
    Generates and returns matrix with distances between all targets and (available weight max villages) at once.
    For example for targets: [T1, T2], weights_max (W1, W2, W3)

    dist matrix would be
    [X11, X12, X13]
    [X21, X22, X23]

    and coord_to_id
    {(coord of T2 - tuple): 0, (coord of T2 - tuple) 1}

    and then having tuple of coords for target, we can get all distances to weights by

    dist_matrix[coord_to_id[coord of target]]
    """
    if not weight_max_lst:
        return None, {}

    coord_to_id = {}
    coords = []
    for target in targets:
        coord = target.coord_tuple()
        if coord in coord_to_id:
            continue
        coord_to_id[coord] = len(coords)
        coords.append(coord)

    if not coords:
        return None, {}

    coords_arr = np.array(coords, dtype=np.float32)
    weight_coords_arr = np.array(
        [i.coord_tuple for i in weight_max_lst], dtype=np.float32
    )
    dist_matrix = cdist(coords_arr, weight_coords_arr, "euclidean")
    return dist_matrix, coord_to_id


def complete_outline_write(outline: Outline, salt: bytes | str | None = None) -> None:
    """
    Auto write out given outline
    1. Fake Rams
    2. Ruins
    3. Nobles
    4. Offs & Ruin offs
    5. Fake Nobles

    For every queryset, forLoop over its targets and
    in each step writting the step's target and updating weights max
    """
    random = SystemRandom(salt)
    outline = (
        Outline.objects.select_related("world")
        .filter(pk=outline.pk)
        .only(
            "pk",
            "morale_on",
            "initial_outline_minimum_noble_troops",
            "initial_outline_minimum_fake_noble_troops",
            "initial_outline_nobles_limit",
            "initial_outline_fake_limit",
            "initial_outline_min_off",
            "initial_outline_max_off",
            "initial_outline_maximum_off_dist",
            "initial_outline_catapult_min_value",
            "initial_outline_catapult_max_value",
            "initial_outline_buildings",
            "initial_outline_front_dist",
            "initial_outline_target_dist",
            "initial_outline_average_ruining_points",
            "initial_outline_min_ruin_attack_off",
            "initial_outline_fake_mode",
            "morale_on_targets_greater_than",
            "mode_off",
            "mode_noble",
            "mode_division",
            "mode_guide",
            "mode_split",
            "night_bonus",
            "enter_t1",
            "enter_t2",
            # For world fields accessed in logic:
            "world_id",
            "world__speed_world",
            "world__speed_units",
            "world__casual_attack_block_ratio",
            "world__morale",
        )
        .get()
    )

    all_targets = list(
        Target.objects.filter(outline=outline)
        .only(
            "pk",
            "target",
            "village_id",
            "player",
            "player_created_at",
            "player_id",
            "points",
            "fake",
            "ruin",
            "required_off",
            "required_noble",
            "exact_off",
            "exact_noble",
            "mode_off",
            "mode_noble",
            "mode_division",
            "mode_guide",
        )
        .order_by("id")
    )

    targets = [target for target in all_targets if not target.ruin and not target.fake]
    fakes = [target for target in all_targets if target.fake and not target.ruin]
    ruins = [target for target in all_targets if target.ruin and not target.fake]

    real_weight_max_lst = list(
        WeightMaximum.objects.filter(outline=outline, too_far_away=False).only(
            "pk",
            "player",
            "start",
            "points",
            "x_coord",
            "y_coord",
            "off_state",
            "off_left",
            "catapult_state",
            "catapult_left",
            "nobleman_state",
            "nobleman_left",
            "ram_left",
            "first_line",
            "player_id",
            "village_id",
        )
    )

    for weight_max in real_weight_max_lst:
        for field in WeightMaximum.CHANGES_TRACKED_FIELDS:
            setattr(
                weight_max, f"_original_{field}", deepcopy(getattr(weight_max, field))
            )

    weight_max_lst = [
        FastWeightMaximum(weight_max, index, outline)
        for index, weight_max in enumerate(real_weight_max_lst)
    ]

    dist_matrix, coord_to_id_in_matrix = generate_distance_matrix(
        weight_max_lst=weight_max_lst, targets=all_targets
    )
    if outline.morale_on:
        morale_dict = generate_morale_dict(outline, all_targets, weight_max_lst)
    else:
        morale_dict = None

    weight_create_lst: list[WeightModel] = []

    create_fakes = CreateWeights(
        random,
        deepcopy(fakes),
        outline,
        weight_max_lst,
        dist_matrix,
        coord_to_id_in_matrix,
        morale_dict,
        weight_create_lst,
        noble=False,
        ruin=False,
    )
    create_fakes()

    create_nobles = CreateWeights(
        random,
        targets,
        outline,
        weight_max_lst,
        dist_matrix,
        coord_to_id_in_matrix,
        morale_dict,
        weight_create_lst,
        noble=True,
        ruin=False,
    )
    create_nobles()

    create_fake_nobles = CreateWeights(
        random,
        fakes,
        outline,
        weight_max_lst,
        dist_matrix,
        coord_to_id_in_matrix,
        morale_dict,
        weight_create_lst,
        noble=True,
        ruin=False,
    )
    create_fake_nobles()

    create_offs = CreateWeights(
        random,
        targets,
        outline,
        weight_max_lst,
        dist_matrix,
        coord_to_id_in_matrix,
        morale_dict,
        weight_create_lst,
        noble=False,
        ruin=False,
    )
    create_offs()

    create_ruin_offs = CreateWeights(
        random,
        ruins,
        outline,
        weight_max_lst,
        dist_matrix,
        coord_to_id_in_matrix,
        morale_dict,
        weight_create_lst,
        noble=False,
        ruin=False,
    )
    create_ruin_offs()

    create_ruins = CreateWeights(
        random,
        ruins,
        outline,
        weight_max_lst,
        dist_matrix,
        coord_to_id_in_matrix,
        morale_dict,
        weight_create_lst,
        noble=False,
        ruin=True,
    )
    create_ruins()

    WeightModel.objects.bulk_create(weight_create_lst, batch_size=1000)

    for fast_weight_max in weight_max_lst:
        weight_max = real_weight_max_lst[fast_weight_max.index]
        for field in WeightMaximum.CHANGES_TRACKED_FIELDS:
            setattr(weight_max, field, getattr(fast_weight_max, field))

    WeightMaximum.objects.bulk_update(
        [weight for weight in real_weight_max_lst if weight.has_changed is True],
        fields=[
            "off_state",
            "off_left",
            "catapult_state",
            "catapult_left",
            "nobleman_state",
            "nobleman_left",
        ],
        batch_size=500,
    )


class CreateWeights:
    def __init__(
        self,
        random: SystemRandom,
        targets: list[Target],
        outline: Outline,
        weight_max_list: list[FastWeightMaximum],
        dist_matrix: "NDArray | None",
        coord_to_id_in_matrix: dict[tuple[int, int], int],
        morale_dict: defaultdict[tuple[str, str], int] | None,
        weight_create_lst: list[WeightModel],
        noble: bool = False,
        ruin: bool = False,
    ) -> None:
        self.random = random
        self.targets: list[Target] = targets
        self.outline: Outline = outline
        self.noble: bool = noble
        self.ruin: bool = ruin
        self.morale_dict = morale_dict
        self.dist_matrix = dist_matrix
        self.coord_to_id_in_matrix = coord_to_id_in_matrix
        self.modes_list = ["closest", "close", "random", "far"]
        self.weight_create_lst = weight_create_lst
        self.weight_max_list = weight_max_list

    @staticmethod
    def _is_syntax_extended(target: Target, noble_or_ruin: bool = False) -> bool:
        if noble_or_ruin:
            if len(target.exact_noble) == 4:
                return True
            return False
        if len(target.exact_off) == 4:
            return True
        return False

    def _extended_syntax(
        self, target: Target, noble_or_ruin: bool = False
    ) -> Generator[tuple[int, str]]:
        # closest, close, random, far

        if noble_or_ruin:
            yield from zip(target.exact_noble, self.modes_list)
        else:
            yield from zip(target.exact_off, self.modes_list)

    def _noble_write(self, target: Target) -> None:
        if self._is_syntax_extended(target, noble_or_ruin=True):
            self._annotate_distances_and_morale_for_target(target)
            for required, mode in self._extended_syntax(target, noble_or_ruin=True):
                if required == 0:
                    continue
                target.required_noble = required
                target.mode_noble = mode
                weight_noble: WriteNobleTarget = WriteNobleTarget(
                    random=self.random,
                    target=target,
                    outline=self.outline,
                    weight_max_list=self.weight_max_list,
                )
                self.weight_create_lst += weight_noble.weight_create_list()

        elif target.required_noble > 0:
            self._annotate_distances_and_morale_for_target(target)
            weight_noble = WriteNobleTarget(
                random=self.random,
                target=target,
                outline=self.outline,
                weight_max_list=self.weight_max_list,
            )
            self.weight_create_lst += weight_noble.weight_create_list()

    def _ruin_write(self, target: Target) -> None:
        if self._is_syntax_extended(target, noble_or_ruin=True):
            self._annotate_distances_and_morale_for_target(target)
            for required, mode in self._extended_syntax(target, noble_or_ruin=True):
                if required == 0:
                    continue
                target.required_off = required
                target.mode_off = mode
                weight_ram: WriteRamTarget = WriteRamTarget(
                    random=self.random,
                    target=target,
                    outline=self.outline,
                    weight_max_list=self.weight_max_list,
                    ruin=True,
                )
                self.weight_create_lst += weight_ram.weight_create_list()

        else:
            target.required_off = target.required_noble
            if target.required_off > 0:
                self._annotate_distances_and_morale_for_target(target)
                weight_ram = WriteRamTarget(
                    random=self.random,
                    target=target,
                    outline=self.outline,
                    weight_max_list=self.weight_max_list,
                    ruin=True,
                )
                self.weight_create_lst += weight_ram.weight_create_list()

    def _ram_write(self, target: Target) -> None:
        if self._is_syntax_extended(target, noble_or_ruin=False):
            self._annotate_distances_and_morale_for_target(target)
            for required, mode in self._extended_syntax(target, noble_or_ruin=False):
                if required == 0:
                    continue
                target.required_off = required
                target.mode_off = mode
                weight_ram: WriteRamTarget = WriteRamTarget(
                    random=self.random,
                    target=target,
                    outline=self.outline,
                    weight_max_list=self.weight_max_list,
                    ruin=False,
                )
                self.weight_create_lst += weight_ram.weight_create_list()

        elif target.required_off > 0:
            self._annotate_distances_and_morale_for_target(target)
            weight_ram = WriteRamTarget(
                random=self.random,
                target=target,
                outline=self.outline,
                weight_max_list=self.weight_max_list,
                ruin=False,
            )
            self.weight_create_lst += weight_ram.weight_create_list()

    def _annotate_distances_and_morale_for_target(self, target: Target) -> None:
        if self.dist_matrix is not None:
            target_coord = target.coord_tuple()
            target_row_in_C = self.coord_to_id_in_matrix[target_coord]
            for index, distance in enumerate(
                self.dist_matrix[target_row_in_C].tolist()
            ):
                self.weight_max_list[index].distance = distance
                if self.morale_dict is not None:
                    morale = self.morale_dict[
                        (target.player, self.weight_max_list[index].player)
                    ]
                    self.weight_max_list[index].morale = morale

    def __call__(self):
        target: Target
        for target in self.targets:
            original_required_off = target.required_off
            original_required_noble = target.required_noble
            original_mode_noble = target.mode_noble
            original_mode_off = target.mode_off

            if self.noble:
                self._noble_write(target)
            elif self.ruin:
                self._ruin_write(target)
            else:
                self._ram_write(target)

            target.required_off = original_required_off
            target.required_noble = original_required_noble
            target.mode_noble = original_mode_noble
            target.mode_off = original_mode_off
