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

from copy import deepcopy
from secrets import SystemRandom
from typing import Any, Generator

import numpy as np
from django.db.models.query import QuerySet
from numpy.typing import NDArray
from scipy.spatial.distance import cdist

from base import models
from base.models import Outline
from base.models import TargetVertex as Target
from base.models import WeightModel
from base.models.weight_maximum import WeightMaximum
from utils.write_noble_target import WriteNobleTarget
from utils.write_ram_target import WriteRamTarget


def generate_distance_matrix(
    outline: models.Outline, weight_max_lst: list[WeightMaximum]
):
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
    targets: QuerySet["Target"] = models.TargetVertex.objects.filter(
        outline=outline
    ).order_by("id")

    coord_to_id = {}
    list_of_coords = []
    for target in targets.only("target"):
        coord = target.coord_tuple()
        if coord in coord_to_id:
            continue
        list_coords_len = len(list_of_coords)
        coord_to_id[coord] = list_coords_len
        list_of_coords.append(np.array(coord))

    if not len(list_of_coords):
        return None, {}

    dist_matrix = cdist(
        np.array(list_of_coords),
        np.array([np.array(i.coord_tuple()) for i in weight_max_lst]),
        "euclidean",
    )
    return dist_matrix, coord_to_id


def get_targets(outline: Outline, fake: bool, ruin: bool) -> QuerySet[Target]:
    return Target.objects.filter(outline=outline, fake=fake, ruin=ruin).order_by("id")


def complete_outline_write(outline: models.Outline, salt: bytes | str | None = None):
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

    targets = get_targets(outline, False, False)
    fakes = get_targets(outline, True, False)
    ruins = get_targets(outline, False, True)
    weight_max_lst = list(
        WeightMaximum.objects.filter(outline=outline, too_far_away=False)
    )

    for weight_max in weight_max_lst:
        for field in WeightMaximum.CHANGES_TRACKED_FIELDS:
            setattr(
                weight_max, f"_original_{field}", deepcopy(getattr(weight_max, field))
            )

    dist_matrix, coord_to_id_in_matrix = generate_distance_matrix(
        outline=outline, weight_max_lst=weight_max_lst
    )
    create_fakes = CreateWeights(
        random,
        fakes,
        outline,
        weight_max_lst,
        dist_matrix,
        coord_to_id_in_matrix,
        noble=False,
        ruin=False,
    )
    weight_max_lst = create_fakes()

    create_ruins = CreateWeights(
        random,
        ruins,
        outline,
        weight_max_lst,
        dist_matrix,
        coord_to_id_in_matrix,
        noble=False,
        ruin=True,
    )
    weight_max_lst = create_ruins()

    create_nobles = CreateWeights(
        random,
        targets,
        outline,
        weight_max_lst,
        dist_matrix,
        coord_to_id_in_matrix,
        noble=True,
        ruin=False,
    )
    weight_max_lst = create_nobles()

    create_offs = CreateWeights(
        random,
        targets,
        outline,
        weight_max_lst,
        dist_matrix,
        coord_to_id_in_matrix,
        noble=False,
        ruin=False,
    )
    weight_max_lst = create_offs()

    create_ruin_offs = CreateWeights(
        random,
        ruins,
        outline,
        weight_max_lst,
        dist_matrix,
        coord_to_id_in_matrix,
        noble=False,
        ruin=False,
    )
    weight_max_lst = create_ruin_offs()

    create_fake_nobles = CreateWeights(
        random,
        fakes,
        outline,
        weight_max_lst,
        dist_matrix,
        coord_to_id_in_matrix,
        noble=True,
        ruin=False,
    )
    weight_max_lst = create_fake_nobles()
    WeightMaximum.objects.bulk_update(
        [weight for weight in weight_max_lst if weight.has_changed is True],
        fields=[
            "off_state",
            "off_left",
            "catapult_state",
            "catapult_left",
            "nobleman_state",
            "nobleman_left",
            "fake_limit",
        ],
        batch_size=1000,
    )


class CreateWeights:
    def __init__(
        self,
        random: SystemRandom,
        targets: QuerySet[Target],
        outline: Outline,
        weight_max_list: list[WeightMaximum],
        dist_matrix: NDArray[np.floating[Any]] | None,
        coord_to_id_in_matrix: dict[tuple[int, int], int],
        noble: bool = False,
        ruin: bool = False,
    ) -> None:
        self.random = random
        self.targets: QuerySet[Target] = targets
        self.outline: Outline = outline
        self.noble: bool = noble
        self.ruin: bool = ruin
        self.dist_matrix = dist_matrix
        self.coord_to_id_in_matrix = coord_to_id_in_matrix
        self.modes_list = ["closest", "close", "random", "far"]
        self.weight_create_lst: list[WeightModel] = []
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
    ) -> Generator[tuple[int, str], None, None]:
        # closest, close, random, far

        if noble_or_ruin:
            iterator = zip(target.exact_noble, self.modes_list)
        else:
            iterator = zip(target.exact_off, self.modes_list)
        required: int
        for required, mode in iterator:
            yield (required, mode)

    def _create_weights_or_pass_update_max_list(
        self, weights_lsts: tuple[list[WeightModel], list[WeightMaximum]]
    ) -> None:
        # note that we hit database only when have a lot of data
        temp_to_update_dict = {}
        weight_max: WeightMaximum
        for weight_max in weights_lsts[1]:
            temp_to_update_dict[weight_max.pk] = weight_max

        for i, weight_max in enumerate(self.weight_max_list):

            if weight_max.pk in temp_to_update_dict:
                self.weight_max_list[i] = temp_to_update_dict[weight_max.pk]

        weight: WeightModel
        for weight in weights_lsts[0]:
            self.weight_create_lst.append(weight)

    def _noble_write(self, target: Target) -> None:
        if self._is_syntax_extended(target, noble_or_ruin=True):
            self._annotate_distances_for_target(target)
            for (required, mode) in self._extended_syntax(target, noble_or_ruin=True):
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
                self._create_weights_or_pass_update_max_list(
                    weight_noble.weight_create_list()
                )

        else:
            if target.required_noble > 0:
                self._annotate_distances_for_target(target)
                weight_noble: WriteNobleTarget = WriteNobleTarget(
                    random=self.random,
                    target=target,
                    outline=self.outline,
                    weight_max_list=self.weight_max_list,
                )
                self._create_weights_or_pass_update_max_list(
                    weight_noble.weight_create_list()
                )

    def _ruin_write(self, target: Target) -> None:
        if self._is_syntax_extended(target, noble_or_ruin=True):
            self._annotate_distances_for_target(target)
            for (required, mode) in self._extended_syntax(target, noble_or_ruin=True):
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
                self._create_weights_or_pass_update_max_list(
                    weight_ram.weight_create_list()
                )

        else:
            target.required_off = target.required_noble
            if target.required_off > 0:
                self._annotate_distances_for_target(target)
                weight_ram: WriteRamTarget = WriteRamTarget(
                    random=self.random,
                    target=target,
                    outline=self.outline,
                    weight_max_list=self.weight_max_list,
                    ruin=True,
                )
                self._create_weights_or_pass_update_max_list(
                    weight_ram.weight_create_list()
                )

    def _ram_write(self, target: Target) -> None:
        if self._is_syntax_extended(target, noble_or_ruin=False):
            self._annotate_distances_for_target(target)
            for (required, mode) in self._extended_syntax(target, noble_or_ruin=False):
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
                self._create_weights_or_pass_update_max_list(
                    weight_ram.weight_create_list()
                )

        else:
            if target.required_off > 0:
                self._annotate_distances_for_target(target)
                weight_ram: WriteRamTarget = WriteRamTarget(
                    random=self.random,
                    target=target,
                    outline=self.outline,
                    weight_max_list=self.weight_max_list,
                    ruin=False,
                )
                self._create_weights_or_pass_update_max_list(
                    weight_ram.weight_create_list()
                )

    def _annotate_distances_for_target(self, target: Target) -> None:
        if self.dist_matrix is not None:
            target_coord = target.coord_tuple()
            target_row_in_C = self.coord_to_id_in_matrix[target_coord]
            for index, distance in enumerate(self.dist_matrix[target_row_in_C]):
                setattr(self.weight_max_list[index], "distance", distance)

    def __call__(self) -> list[WeightMaximum]:
        # note that .iterator() prevents from caching querysets
        # which can possibly cause overwriting some targets attributes

        target: Target
        for target in self.targets.iterator():
            if self.noble:
                self._noble_write(target)
            elif self.ruin:
                self._ruin_write(target)
            else:
                self._ram_write(target)

        WeightModel.objects.bulk_create(self.weight_create_lst, batch_size=2000)
        return self.weight_max_list
