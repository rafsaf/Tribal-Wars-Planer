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

from collections.abc import Sequence
from typing import Any, Literal


class CDistBrute:
    def __init__(
        self,
        # usually list of 2D villages tuple (x, y) coordinates
        ally_villages: Sequence[Sequence[Any]],
        enemy_villages: Sequence[Sequence[Any]],
        min_radius: float,
        max_radius: float,
    ) -> None:
        import numpy as np

        self.all_ally = np.array(ally_villages, dtype=np.float32)
        self.all_ally.flags.writeable = False
        self.all_enemy = np.array(enemy_villages, dtype=np.float32)
        self.all_enemy.flags.writeable = False
        self.min_radius = min_radius
        self.max_radius = max_radius

    def triple_result(
        self, batch_size: int = 36, mode: Literal["for", "numpy"] = "for"
    ) -> tuple[set[tuple[int, int]], set[tuple[int, int]], set[tuple[int, int]]]:
        import numpy as np
        from scipy.spatial.distance import cdist

        """
        Brute force. This is detailed version of result method.

        Returns
        -------
        tuple of np.ndarray is returned:

        (below `x` is minimum of distances to every enemy village)

        `front_lst` : array with coords `x <= min_radius`

        `back_lst` : array with coord `min_radius < x < max_radius`

        `away_lst` : array with coords `min_radius >= max_radius`

        NOTES
        -----
        For given in class init enemy villages `N` and ally villages `M`
        - Step 1: Iterate over the `M` in `i` batches `k` of size `batch_size` where `i` is ceil from `len(M)/batch_size`
        - Step 2: For every batch k1, k2 calculate matrix of sq euclidean distances k x N allies from enemies
        - Step 3: Append villages in to front, back or away list
        """

        sq_min_radius = np.float32(self.min_radius**2)
        sq_max_radius = np.float32(self.max_radius**2)

        total_front: set[tuple[int, int]] = set()
        total_back: set[tuple[int, int]] = set()
        total_away: set[tuple[int, int]] = set()

        if mode == "for":
            for i in range(int(np.ceil(len(self.all_ally) / batch_size))):
                batch_ally = self.all_ally[i * batch_size : (i + 1) * batch_size]

                C = cdist(batch_ally, self.all_enemy, "sqeuclidean").min(axis=1)

                for index, x in np.ndenumerate(C):
                    if x <= sq_min_radius:
                        total_front.add(tuple(batch_ally[index]))
                    elif x >= sq_max_radius:
                        total_away.add(tuple(batch_ally[index]))
                    else:
                        total_back.add(tuple(batch_ally[index]))

        if mode == "numpy":
            for i in range(int(np.ceil(len(self.all_ally) / batch_size))):
                batch_ally = self.all_ally[i * batch_size : (i + 1) * batch_size]

                C = cdist(batch_ally, self.all_enemy, "sqeuclidean").min(axis=1)

                mask_front = C <= sq_min_radius
                mask_away = C >= sq_max_radius
                mask_back = np.logical_not(mask_front | mask_away)
                total_back.update(map(tuple, batch_ally[mask_back].astype(np.int32)))
                total_front.update(map(tuple, batch_ally[mask_front].astype(np.int32)))
                total_away.update(map(tuple, batch_ally[mask_away].astype(np.int32)))

        return (total_front, total_back, total_away)
