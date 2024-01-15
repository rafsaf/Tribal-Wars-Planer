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

from collections import Counter
from functools import cached_property
from typing import TypedDict

from base.models import Outline, TargetVertex
from utils.basic.mode import TargetMode


class TargetDuplicateInfo(TypedDict):
    target: str
    duplicate: int
    lines: str


class TargetBarbarianInfo(TypedDict):
    target: str
    lines: str


class TargetsCalculations:
    def __init__(self, outline: Outline, target_mode: TargetMode) -> None:
        self.outline: Outline = outline
        self.target_mode: TargetMode = target_mode
        self.all_targets = list(
            TargetVertex.objects.filter(outline=outline).order_by("pk")
        )

    @cached_property
    def _real_targets(self) -> list[TargetVertex]:
        return [
            target for target in self.all_targets if not target.fake and not target.ruin
        ]

    @cached_property
    def _fake_targets(self) -> list[TargetVertex]:
        return [
            target for target in self.all_targets if target.fake and not target.ruin
        ]

    @cached_property
    def _ruin_targets(self) -> list[TargetVertex]:
        return [
            target for target in self.all_targets if not target.fake and target.ruin
        ]

    def actual_targets(self) -> list[TargetVertex]:
        if self.target_mode.is_real:
            return self._real_targets
        elif self.target_mode.is_fake:
            return self._fake_targets
        else:
            return self._ruin_targets

    @property
    def len_real(self) -> int:
        return len(self._real_targets)

    @property
    def len_fake(self) -> int:
        return len(self._fake_targets)

    @property
    def len_ruin(self) -> int:
        return len(self._ruin_targets)

    @property
    def actual_len(self) -> int:
        if self.target_mode.is_real:
            return self.len_real
        elif self.target_mode.is_fake:
            return self.len_fake
        else:
            return self.len_ruin

    @staticmethod
    def _targets_duplicates(
        targets: list[TargetVertex],
    ) -> list[TargetDuplicateInfo]:
        """
        Example result:
        ===============

        [
            {"target": "500|500", duplicate: 2, lines: "2,3"},
            {"target": "500|501", duplicate: 4, lines: "5,6,7..."}
        ]

        """

        targets_context: dict[str, list[str]] = {}
        # example {"500|500": [1, 2, 3]}
        # where 1,2,3 represent line numbers in target input
        result: list[TargetDuplicateInfo] = []

        for i, target in enumerate(targets):
            if target.target in targets_context:
                if len(targets_context[target.target]) < 4:
                    targets_context[target.target].append(str(i + 1))
            else:
                targets_context[target.target] = [str(i + 1)]

        target_counter = Counter([target.target for target in targets])

        for target_coord, count in target_counter.items():
            if count == 1:
                continue
            line_lst: list[str] = targets_context[target_coord]
            if len(line_lst) <= 3:
                lines: str = ",".join(line_lst)
            else:
                lines = ",".join(line_lst[:3]) + ",..."
            result.append(
                {
                    "target": target_coord,
                    "duplicate": count,
                    "lines": lines,
                }
            )

        return result

    @staticmethod
    def _barbarians(
        targets: list[TargetVertex],
    ) -> list[TargetBarbarianInfo]:
        """
        Example result:
        ===============

        [
            {"target": "500|500", lines: "2,3"},
            {"target": "500|501", lines: "5,6,7..."}
        ]

        """

        targets_context: dict[str, list[str]] = {}
        # example {"500|500": [1, 2, 3]}
        # where 1,2,3 represent line numbers in target input
        result: list[TargetBarbarianInfo] = []

        for i, target in enumerate(targets):
            if target.player:
                # skip targets with player name set
                continue
            if target.target in targets_context:
                if len(targets_context[target.target]) < 4:
                    targets_context[target.target].append(str(i + 1))
            else:
                targets_context[target.target] = [str(i + 1)]

        for target_coord, line_lst in targets_context.items():
            if len(line_lst) <= 3:
                lines: str = ",".join(line_lst)
            else:
                lines = ",".join(line_lst[:3]) + ",..."
            result.append(
                {
                    "target": target_coord,
                    "lines": lines,
                }
            )

        return result

    @cached_property
    def real_duplicates(self) -> list[TargetDuplicateInfo]:
        return self._targets_duplicates(self._real_targets)

    @cached_property
    def fake_duplicates(self) -> list[TargetDuplicateInfo]:
        return self._targets_duplicates(self._fake_targets)

    @cached_property
    def ruin_duplicates(self) -> list[TargetDuplicateInfo]:
        return self._targets_duplicates(self._ruin_targets)

    def show_duplicates(self) -> bool:
        return (
            len(self.real_duplicates) > 0
            or len(self.fake_duplicates) > 0
            or len(self.ruin_duplicates) > 0
        )

    @cached_property
    def real_barbarians(self) -> list[TargetBarbarianInfo]:
        return self._barbarians(self._real_targets)

    @cached_property
    def fake_barbarians(self) -> list[TargetBarbarianInfo]:
        return self._barbarians(self._fake_targets)

    @cached_property
    def ruin_barbarians(self) -> list[TargetBarbarianInfo]:
        return self._barbarians(self._ruin_targets)

    def show_barbarians(self) -> bool:
        return (
            len(self.real_barbarians) > 0
            or len(self.fake_barbarians) > 0
            or len(self.ruin_barbarians) > 0
        )
